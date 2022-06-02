#!/usr/bin/python3

import argparse
import sys
import warnings
import logging
from requests import exceptions
import traceback
import requests
from requests.exceptions import HTTPError, ConnectionError

import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.core import ErmrestCatalog, get_credential, format_exception
from deriva.core.utils import eprint
from deriva.core.base_cli import BaseCLI
from deriva.utils.catalog.components.model_elements import DerivaModel, DerivaCatalog, DerivaSchema, DerivaTable
from deriva.utils.catalog.version import __version__ as VERSION

logger = logging.getLogger(__name__)

IS_PY2 = (sys.version_info[0] == 2)
IS_PY3 = (sys.version_info[0] == 3)

if IS_PY3:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

chaise_tags.catalog_config = 'tag:isrd.isi.edu,2019:catalog-config'

logger = logging.getLogger(__name__)

class DerivaConfigError(Exception):
    def __init__(self, msg):
        self.msg = msg


class DerivaCatalogConfigure(DerivaCatalog):
    def __init__(self, host, scheme='https', catalog_id=1, model=None):
        super(DerivaCatalogConfigure, self).__init__(host, scheme=scheme, catalog_id = catalog_id)

    def _make_schema_instance(self, schema_name):
        return DerivaSchemaConfigure(self, schema_name)

    def configure_ermrest_client(self, groups):
        """
        Set up ermrest_client table so that it has readable names and uses the display name of the user as the row name.
        :param groups:
        :return:
        """
        with DerivaModel(self) as m:

            #ermrest_client = m.table('public', 'ERMrest_Client')
            ermrest_client = m.catalog.model.schemas['public'].tables['ERMrest_Client']

            # Make ermrest_client table visible.  If the GUID or member name is considered sensitivie, then this needs to be
            # changed.
            ermrest_client.acls['select'] = ['*']

            # Set table and row name.
            ermrest_client.annotations.update({
                chaise_tags.display: {'name': 'Users'},
                chaise_tags.visible_columns: {'compact': ['ID', 'Full_Name', 'Display_Name', 'Email']},
                chaise_tags.table_display: {'row_name': {'row_markdown_pattern': '{{{Full_Name}}}'}}
            })

            column_annotations = {
                'RCT': {chaise_tags.display: {'name': 'Creation Time'}},
                'RMT': {chaise_tags.display: {'name': 'Modified Time'}},
                'RCB': {chaise_tags.display: {'name': 'Created By'}},
                'RMB': {chaise_tags.display: {'name': 'Modified By'}}
            }
            for k, v in column_annotations.items():
                ermrest_client.column_definitions[k].annotations.update(v)
            return

    def _configure_www_schema(self):
        """
        Set up a new schema and tables to hold web-page like content.  The tables include a page table, and a asset
        table that can have images that are referred to by the web page.  Pages are written using markdown.
        :return:
        """
        logging.info('Configuring WWW schema')
        # Create a WWW schema if one doesn't already exist.
        try:
            www_schema_def = em.Schema.define('WWW', comment='Schema for tables that will be displayed as web content')
            www_schema = self.model.create_schema(self.catalog, www_schema_def)
        except ValueError as e:
            if 'already exists' not in e.args[0]:
                raise
            else:
                www_schema = self.model.schemas['WWW']

        # Create the page table
        page_table_def = em.Table.define(
            'Page',
            column_defs=[
                em.Column.define('Title', em.builtin_types['text'], nullok=False, comment='Unique title for the page'),
                em.Column.define('Content', em.builtin_types['markdown'], comment='Content of the page in markdown')
            ],
            key_defs=[em.Key.define(['Title'], [['WWW', 'Page_Title_key']])],
            annotations={
                chaise_tags.table_display: {'detailed': {'hide_column_headers': True, 'collapse_toc_panel': True}
                                            },
                chaise_tags.visible_foreign_keys: {'detailed': {}},
                chaise_tags.visible_columns: {'detailed': ['Content']}}
        )
        try:
            www_schema.create_table(self.catalog, page_table_def)
        except ValueError as e:
            if 'already exists' not in e.args[0]:
                raise
        table = DerivaTableConfigure(self, 'WWW', 'Page')
        table.configure_table_defaults()

        # Now set up the asset table
        try:
            table = self.schema('WWW').table('Page')
            table.create_asset_table('RID')
        except ValueError as e:
            if 'already exists' not in e.args[0]:
                raise

        return self

    def set_core_groups(self, catalog_name=None, admin=None, curator=None, writer=None, reader=None,
                        replace=False):
        """
        Look in the catalog to get the group IDs for the four core groups used in the baseline configuration. There are
        three options:  1) core group name can be provided explicitly, 2) group name can be formed from a catalog
        name and a default group name, 3) group name can be formed from the host name and a default group name.
        :param catalog_name: Name of the catalog to use as a prefix in looking up default name of the group. Default
               group names are formed by combining the catalog_name with the standard group name: e.g. foo-admin
               foo-writer, and foo-reader
        :param admin: Group name to use in place of default
        :param curator: Group name to use in place of default
        :param writer: Group name to use in lace of default
        :param reader: Either '*' for anonymous read access, or the group name to use in place of default
        :param replace: Ignore existing catalog config and use provided arguements.
        :return: dictionary with the four group ids.
        """
        groups = {}
        # Get previous catalog configuration values if they exist
        if chaise_tags.catalog_config in self.model.annotations and not replace:
            groups.update({
                'admin': self.model.annotations[chaise_tags.catalog_config]['groups']['admin'],
                'curator': self.model.annotations[chaise_tags.catalog_config]['groups']['curator'],
                'writer': self.model.annotations[chaise_tags.catalog_config]['groups']['writer'],
                'reader': self.model.annotations[chaise_tags.catalog_config]['groups']['reader']
            })
        else:
            if admin == '*' or curator == '*' or writer == '*':
                raise DerivaConfigError(msg='Only reader may be anonymous when setting core catalog groups')
            if not catalog_name and (admin is None or curator is None or writer is None or reader is None):
                raise DerivaConfigError(msg='Catalog name required to look up group')

            if admin is None:
                admin = catalog_name + '-admin'
            if curator is None:
                curator = catalog_name + '-curator'
            if writer is None:
                writer = catalog_name + '-writer'
            if reader is None:
                reader = catalog_name + '-reader'

            pb = self.getPathBuilder()
            catalog_groups = {i['Display_Name']: i for i in pb.public.ERMrest_Group.entities()}
            groups = {}
            try:
                groups.update({
                    'admin': catalog_groups[admin]['ID'],
                    'curator': catalog_groups[curator]['ID'],
                    'writer': catalog_groups[writer]['ID'],
                    'reader': catalog_groups[reader]['ID'] if reader is not '*' else '*'
                })
            except KeyError as e:
                raise DerivaConfigError(msg='Group {} not defined'.format(e.args[0]))

        return groups

    def configure_group_table(self, groups):
        """
        Create a table in the public schema for tracking mapping of group names.
        :param groups:
        :return:
        """

        logging.info('Configuring groups')
        ermrest_group = self.model.schemas['public'].tables['ERMrest_Group']

        # Make ERMrest_Group table visible to writers, curators, and admins.
        ermrest_group.acls['select'] = [groups['writer'], groups['curator'], groups['admin']]

        # Set table and row name.
        ermrest_group.annotations.update({
            chaise_tags.display: {'name': 'Globus Group'},
            chaise_tags.visible_columns: {'*': ['Display_Name', 'Description', 'URL', 'ID']},
            chaise_tags.table_display: {'row_name': {'row_markdown_pattern': '{{{Display_Name}}}'}}
        })

        # Set compound key so that we can link up with Visible_Group table.
        try:
            ermrest_group.create_key(
                self.catalog,
                em.Key.define(['ID', 'URL', 'Display_Name', 'Description'],
                              constraint_names=[('public', 'ERMrest_Group_ID_URL_Display_Name_Description_key')],
                              comment='Group ID is unique.'

                              )
            )
        except exceptions.HTTPError as e:
            if 'already exists' not in e.args[0]:
                raise

        # Create a catalog groups table
        column_defs = [
            em.Column.define('Display_Name', em.builtin_types['text']),
            em.Column.define('URL', em.builtin_types['text'],
                             annotations={
                                 chaise_tags.column_display: {
                                     '*': {'markdown_pattern': '[**{{Display_Name}}**]({{{URL}}})'}},
                                 chaise_tags.display: {'name': 'Group Management Page'}
                             }
                             ),
            em.Column.define('Description', em.builtin_types['text']),
            em.Column.define('ID', em.builtin_types['text'], nullok=False)
        ]

        key_defs = [
            em.Key.define(['ID'],
                          constraint_names=[('public', 'Catalog_Group_ID_key')]),
            em.Key.define(['ID','URL','Display_Name','Description'],
                          constraint_names=[('public', 'Catalog_Group_ID_URL_Display_Name_Description_key')],
                          comment='Key to ensure that group only is entered once.'
                          ),
        ]

        # Set up a foreign key to the group table so that the creator of a record can only select
        # groups of which they are members of for values of the Owners column.
        fkey_group_policy = {
            # FKey to group can be created only if you are a member of the group you are referencing
            'set_owner': {"types": ["insert"],
                          "projection": ["ID"],
                          "projection_type": "acl"}
        }

        # Allow curators to also update the foreign key.
        fkey_group_acls = {"insert": [groups['curator']], "update": [groups['curator']]}

        # Create a foreign key to the group table. Set update policy to keep group entry in sync.
        fkey_defs = [
            em.ForeignKey.define(['ID', 'URL', 'Display_Name', 'Description'],
                                 'public', 'ERMrest_Group', ['ID', 'URL', 'Display_Name', 'Description'],
                                 on_update='CASCADE',
                                 acls=fkey_group_acls,
                                 acl_bindings=fkey_group_policy,
                                 )
        ]

        # Create the visible groups table. Set ACLs so that writers or curators can add entries or edit.  Allow writers
        # to be able to create new entries.  No one is allowed to update, as this is only done via the CASCADE.
        catalog_group = em.Table.define(
            'Catalog_Group',
            annotations={
                chaise_tags.table_display: {'row_name': {'row_markdown_pattern': '{{{Display_Name}}}'}}},
            column_defs=column_defs,
            fkey_defs=fkey_defs, key_defs=key_defs,
            acls={
                # Make ERMrest_Group table visible to members of the group members, curators, and admins.
                'select': [groups['reader']],
                'insert': [groups['writer'], groups['curator']]
            },
        )

        public_schema = self.model.schemas['public']

        # Get or create Catalog_Group table....
        try:
            public_schema.create_table(self.catalog, catalog_group)
        except ValueError as e:
            if 'already exists' not in e.args[0]:
                raise
        table = DerivaTableConfigure(self, 'public', 'Catalog_Group')
        table.configure_table_defaults(set_policy=False)
        return

    def configure_baseline_catalog(self,
                                   catalog_name=None,
                                   admin=None, curator=None, writer=None, reader=None,
                                   set_policy=True,
                                   public=False):
        """
        Put catalog into standard configuration which includes:
        1) Setting default display mode to be to turn underscores to spaces.
        2) Set access control assuming admin, curator, writer, and reader groups.
        3) Configure ermrest_client to have readable names.

        :param catalog_name:
        :param admin: Name of the admin group.  Defaults to catalog-admin
        :param curator: Name of the curator group. Defaults to catalog-curator
        :param writer: Name of the writer group. Defaults to catalog-writer
        :param reader: Name of the reader group. Defaults to catalog-reader
        :param set_policy: Set policy for catalog to support reader/writer/curator/admin groups.
        :param public: Set to true if anonymous read access should be allowed.
        :param apply: If true then applyt the changes from the model to the catalog
        :return:
        """

        if not catalog_name:
            # If catalog name is not provided, default to the host name of the host.
            catalog_name = urlparse(self.catalog.get_server_uri()).hostname.split('.')[0]
        groups = self.set_core_groups(catalog_name=catalog_name,
                                      admin=admin, curator=curator, writer=writer, reader=reader)
        with DerivaModel(self) as m:
            model = m.model()
            # Record configuration of catalog so we can retrieve when we configure tables later on.
            model.annotations[chaise_tags.catalog_config] = {'name': catalog_name, 'groups': groups}

            # Set up default name style for all schemas.
            for s in model.schemas.values():
                s.annotations[chaise_tags.display] = {'name_style': {'underline_space': True}}

            # modify catalog ACL config to support basic admin/curator/writer/reader access.
            if set_policy:
                model.acls.update({
                    "owner": [groups['admin'], 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'],
                    "insert": [groups['curator'], groups['writer']],
                    "update": [groups['curator']],
                    "delete": [groups['curator']],
                    "select": [groups['writer'], groups['reader']] if not public else ['*'],
                    "enumerate": ["*"],
                })

            self.configure_ermrest_client(groups)
            self.configure_group_table(groups)
            self._configure_www_schema()

        return


def update_group_table(catalog):
    def group_urls(group):
        guid = group.split('/')[-1]
        link = 'https://app.globus.org/groups/' + guid
        uri = 'https://auth.globus.org/' + guid
        return link, uri

    pb = catalog.getPathBuilder()
    # Attempt to add URL.  This can go away once we have URL entered by ERMrest.
    pb.public.ERMrest_Group.update(
        [{'RID': i['RID'], 'URL': group_urls(i['ID'])[0]} for i in pb.public.ERMrest_Group.entities()]
    )

class DerivaSchemaConfigure(DerivaSchema):
    def __init__(self, catalog, schema_name):
        super(DerivaSchemaConfigure,self).__init__(catalog, schema_name)

    def _make_table_instance(self, schema_name, table_name):
        return DerivaTableConfigure(self.catalog, schema_name, table_name)

class DerivaTableConfigure(DerivaTable):
    def __init__(self, catalog, schema_name, table_name):
        super(DerivaTableConfigure, self).__init__(catalog, schema_name, table_name)
        return

    def apply(self):
        self.catalog.model.schemas[self.schema_name].tables[self.table_name].apply(self.catalog.catalog)

    def configure_self_serve_policy(self, groups):
        """
        Set up a table so it has a self service policy.  Add an owner column if one is not present, and set the acl
        binding so that it follows the self service policy.

        :param groups: dictionary of core catalog groups
        :return:
        """
        with DerivaModel(self.catalog) as m:
            table = m.model().schemas[self.schema_name].tables[self.table_name]

            # Configure table so that access can be assigned to a group.  This requires that we create a column and
            # establish a foreign key to an entry in the group table.  We will set the access control on the foreign key
            # so that you are only able to delagate access to a the creator of the entity belongs to.
            if 'Owner' not in [i.name for i in table.column_definitions]:
                col_def = em.Column.define('Owner', em.builtin_types['text'], comment='Group that can update the record.')
                table.create_column(self.catalog.catalog, col_def)

            # Now configure the policy on the table...
            self_service_policy = {
                # Set up a policy for the table that allows the creator of the record to update and delete the record.
                "self_service_creator": {
                    "types": ["update", 'delete'],
                    "projection": ["RCB"],
                    "projection_type": "acl"
                },
                # Set up a policy for the table that allows members of the group referenced by the Owner column to
                # update and delete the record.
                'self_service_group': {
                    "types": ["update", "delete"],
                    "projection": ["Owner"],
                    "projection_type": "acl"
                }
            }

            # Make table policy be self service, creators and owners can update.
            table.acl_bindings.update(self_service_policy)

            # Set up a foreign key to the group table on the owners column so that the creator of a record can only
            # select groups of which they are members of for values of the Owners column.
            fkey_group_policy = {
                # FKey to group can be created only if you are a member of the group you are referencing
                'set_owner': {"types": ["update", "insert"],
                              "projection": ["ID"],
                              "projection_type": "acl"}
            }

            # Allow curators to also update the foreign key.
            fkey_group_acls = {"insert": [groups['curator']], "update": [groups['curator']]}

            owner_fkey_name = '{}_Owner_fkey'.format(self.table_name)
            fk_def = em.ForeignKey.define(['Owner'],
                                      'public', 'Catalog_Group', ['ID'],

                                      acls=fkey_group_acls, acl_bindings=fkey_group_policy,
                                      constraint_names=[(self.schema_name, owner_fkey_name)],
                                      )
            # Delete old fkey if there is one laying around....
            for fk in table.foreign_keys:
                if len(fk.foreign_key_columns) == 1 and fk.foreign_key_columns[0]['column_name'] == 'Owner':
                    fk.delete(self.catalog.catalog, table)

            # Now create the foreign key to the group table.
            table.create_fkey(self.catalog.catalog, fk_def)
        return

    def create_default_visible_columns(self, really=False):
        with DerivaModel(self.catalog) as m:
            table = m.model().schemas[self.schema_name].tables[self.table_name]

            if chaise_tags.visible_columns not in table.annotations or really:
                table.annotations[chaise_tags.visible_columns] = self.default_visible_column_list()
            else:
                spec = self.default_visible_column_list()
                if '*' not in table.annotations[chaise_tags.visible_columns]:
                    table.annotations[chaise_tags.visible_columns]['*'] = spec['*']
                if 'entry' not in table.annotations[chaise_tags.visible_columns]:
                    table.annotations[chaise_tags.visible_columns]['entry'] = spec['entry']
        return self

    def default_visible_column_list(self):
        """
        Create a general visible columns annotation spec that would be consistant with what chaise does by default.
        This spec can then be added to a table and edited for user preference.
        :return:
        """
        with DerivaModel(self.catalog) as m:
            table = m.model().schemas[self.schema_name].tables[self.table_name]

            column_names = [i.name for i in table.column_definitions]
            # First go through the list of foreign keys and create a list of key columns and referenced columns. Keep
            # track of columns that are in composite keys so we only output column spec once.
            simple_fkeys, fkeys = {},{}
            skip_columns = []
            for fk in table.foreign_keys:
                ckey = [c['column_name'] for c in fk.foreign_key_columns] # List of names in composite key.
                skip_columns.extend(ckey[1:])
                fkeys[ckey[0]] = fk.names[0]
                if len(ckey) == 1:
                    simple_fkeys[ckey[0]] = fk.names[0]



            # Move Owner column to be right after RMB if they both exist.
            if 'Owner' in column_names and 'RMB' in column_names:
                column_names.insert(column_names.index('RMB') + 1, column_names.pop(column_names.index('Owner')))

            # Entry will convert all FK columns to the associated outbound specs.  For general spec, we will only
            # do FK specs for columns that have single value FK constraints.
            return {
                'entry': [
                    {'source': [{'outbound': fkeys[i]}, 'RID'] if i in fkeys else i}
                    for i in column_names if i not in skip_columns
                ],
                '*': [
                    {'source': [{'outbound': simple_fkeys[i]}, 'RID'] if i in simple_fkeys else i}
                    for i in column_names
                ]
            }

    def configure_table_defaults(self, set_policy=True, public=False, reset_visible_columns=True):
        """
        This function adds the following basic configuration details to an existing table:
        1) Creates a self service modification policy in which creators can update update any row they create.
           Optionally, an Owner column can be provided, which allows the creater of a row to delegate row ownership to
           a specific group.
        2) Adds display annotations and foreign key declarations so that system columns RCB, RMB display in a user
           friendly way.
        :param set_policy: If true, then configure the table to have a self service policy
        :param public: Make table acessible without logging in.
        :return:
        """
        with DerivaModel(self.catalog) as m:
            model = m.model()
            table = model.schemas[self.schema_name].tables[self.table_name]

            if chaise_tags.catalog_config not in model.annotations:
                raise DerivaConfigError(msg='Attempting to configure table before catalog is configured')

            # Hack to update description and URL until we get these passed through ermrest....
            update_group_table(self.catalog)

            schema = model.schemas[self.schema_name]

            if public:
                # First copy dver any inherited ACLS.
                if schema.acls:
                    table.acls.update(schema.acls)
                elif model.acls:
                    table.acls.update(model.acls)
                table.acls.pop("create", None)
                # Now add permision for anyone to read.
                table.acls['select'] = ['*']

            if set_policy:
                self.configure_self_serve_policy(self.catalog.get_groups())

            # Configure schema if not already done so.
            if chaise_tags.display not in schema.annotations:
                schema.annotations[chaise_tags.display] = {}
            if 'name_style' not in schema.annotations[chaise_tags.display]:
                schema.annotations[chaise_tags.display].update({'name_style': {'underline_space': True}})

            # Set up foreign key to ermrest_client on RCB, RMB and Owner. If ermrest_client is configured, the
            # full name of the user will be used for the FK value.
            for col, display in [('RCB', 'Created By'), ('RMB', 'Modified By')]:
                fk_name = '{}_{}_fkey'.format(self.table_name, col)
                # Delete old fkey if there is one laying around....
                for fk in table.foreign_keys:
                    if len(fk.foreign_key_columns) == 1 and fk.foreign_key_columns[0]['column_name'] == col:
                        fk.delete(self.catalog.catalog, table)

                fk_def = em.ForeignKey.define([col],
                                          'public', 'ERMrest_Client', ['ID'],
                                          constraint_names=[(self.schema_name, fk_name)],
                                          )
                table.create_fkey(self.catalog.catalog, fk_def)

                # Add a display annotation so that we have sensible name for RCB and RMB.
                table.column_definitions[col].annotations.update({chaise_tags.display: {'name': display}})

            table.column_definitions['RCT'].annotations.update({chaise_tags.display: {'name': 'Creation Time'}})
            table.column_definitions['RMT'].annotations.update({chaise_tags.display: {'name': 'Modified Time'}})

            self.create_default_visible_columns(really=reset_visible_columns)

        return self


class DerivaConfigureCatalogCLI(BaseCLI):

    def __init__(self, description, epilog):
        super(DerivaConfigureCatalogCLI, self).__init__(description, epilog, VERSION, hostname_required=True)

        # parent arg parser
        parser = self.parser
        parser.add_argument('configure', choices=['catalog', 'table'],
                            help='Choose between configuring a catalog or a specific table')
        parser.add_argument('--catalog-name', default=None, help="Name of catalog (Default:hostname)")
        parser.add_argument('--catalog', default=1, help="ID number of desired catalog (Default:1)")
        parser.add_argument('--table', default=None, metavar='SCHEMA_NAME:TABLE_NAME',
                            help='Name of table to be configured')
        parser.add_argument('--set-policy', default='True', choices=[True, False],
                            help='Access control policy to be applied to catalog or table')
        parser.add_argument('--reader-group', dest='reader', default=None,
                            help='Group name to use for readers. For a catalog named "foo" defaults for foo-reader')
        parser.add_argument('--writer-group', dest='writer', default=None,
                            help='Group name to use for writers. For a catalog named "foo" defaults for foo-writer')
        parser.add_argument('--curator-group', dest='curator', default=None,
                            help='Group name to use for readers. For a catalog named "foo" defaults for foo-curator')
        parser.add_argument('--admin-group', dest='admin', default=None,
                            help='Group name to use for readers. For a catalog named "foo" defaults for foo-admin')
        parser.add_argument('--publish', default=False, action='store_true',
                            help='Make the catalog or table accessible for reading without logging in')

    @staticmethod
    def _get_credential(host_name, token=None):
        if token:
            return {"cookie": "webauthn={t}".format(t=token)}
        else:
            return get_credential(host_name)

    def main(self):

        args = self.parse_cli()
        credentials = self._get_credential(args.host)
        catalog = DerivaCatalogConfigure(args.host, catalog_id=args.catalog)

        try:
            if args.configure == 'catalog':
                logging.info('Configuring catalog {}:{}'.format(args.host, args.catalog))
                cfg = DerivaCatalogConfigure(args.host, catalog_id=args.catalog)
                cfg.configure_baseline_catalog(catalog_name=args.catalog_name,
                                               reader=args.reader, writer=args.writer, curator=args.curator,
                                               admin=args.admin,
                                               set_policy=args.set_policy, public=args.publish)
                cfg.apply()
            if args.table:
                [schema_name, table_name] = args.table.split(':')
                table = catalog.schema(schema_name).table(table_name)
                table.configure_table_defaults(set_policy=args.set_policy, public=args.publish)
                table.apply()
        except DerivaConfigError as e:
            print(e.msg)
        except HTTPError as e:
            if e.response.status_code == requests.codes.unauthorized:
                msg = 'Authentication required for {}'.format(args.host)
            elif e.response.status_code == requests.codes.forbidden:
                msg = 'Permission denied'
            else:
                msg = e
            logging.debug(format_exception(e))
            eprint(msg)
        except RuntimeError as e:
            sys.stderr.write(str(e))
            return 1
        except:
            traceback.print_exc()
            return 1
        finally:
            sys.stderr.write("\n\n")
        return


def main():
    DESC = "DERIVA Configure Catalog Command-Line Interface"
    INFO = "For more information see: https://github.com/informatics-isi-edu/deriva-catalog-manage"
    return DerivaConfigureCatalogCLI(DESC, INFO).main()


if __name__ == '__main__':
    sys.exit(main())
