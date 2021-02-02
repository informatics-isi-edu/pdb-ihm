#if defined(dev)
        {
            "schema": "PDB",
            "table": "ihm_cross_link_pseudo_site",
            "uri": "tag:misd.isi.edu,2015:display",
            "value": {
                "name": "Chemical Crosslinks with Pseudo Sites",
                "comment_display": {
                    "*": {
                        "table_comment_display" : "inline"
                    }
                }
            }
        },
        {
            "schema": "PDB",
            "table": "ihm_cross_link_pseudo_site",
            "uri": "tag:isrd.isi.edu,2016:visible-columns",
            "value": {
                "*": [
                    "RID",
                    {
                        "comment": "A reference to table entry.id.",
                        "markdown_name": "Structure Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_structure_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    "id",
                    {
                        "comment": "A reference to table ihm_cross_link_restraint.id.",
                        "markdown_name": "Restraint Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_restraint_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    {
                        "comment": "A reference to table ihm_model_list.model_id.",
                        "markdown_name": "Model Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_model_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    {
                        "comment": "A reference to table ihm_pseudo_site.id.",
                        "markdown_name": "Pseudo Site Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_pseudo_site_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    [
                        "PDB",
                        "ihm_cross_link_pseudo_site_cross_link_partner_fkey"
                    ],
                    {
                        "comment": "A reference to the uploaded restraint file in the table Entry_Related_File.id.",
                        "markdown_name": "Uploaded Restraint File",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_Entry_Related_File_fkey"
                                ]
                            },
                            "RID"
                        ]
                    }
                ],
                "detailed": [
                    "RID",
                    {
                        "comment": "A reference to table entry.id.",
                        "markdown_name": "Structure Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_structure_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    "id",
                    {
                        "comment": "A reference to table ihm_cross_link_restraint.id.",
                        "markdown_name": "Restraint Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_restraint_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    {
                        "comment": "A reference to table ihm_model_list.model_id.",
                        "markdown_name": "Model Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_model_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    {
                        "comment": "A reference to table ihm_pseudo_site.id.",
                        "markdown_name": "Pseudo Site Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_pseudo_site_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    [
                        "PDB",
                        "ihm_cross_link_pseudo_site_cross_link_partner_fkey"
                    ],
                    {
                        "comment": "A reference to the uploaded restraint file in the table Entry_Related_File.id.",
                        "markdown_name": "Uploaded Restraint File",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_Entry_Related_File_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    [
                        "PDB",
                        "ihm_cross_link_pseudo_site_RCB_fkey"
                    ],
                    [
                        "PDB",
                        "ihm_cross_link_pseudo_site_RMB_fkey"
                    ],
                    "RCT",
                    "RMT",
                    [
                        "PDB",
                        "ihm_cross_link_pseudo_site_Owner_fkey"
                    ]
                ],
                "entry": [
                    {
                        "comment": "A reference to table entry.id.",
                        "markdown_name": "Structure Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_structure_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    "id",
                    {
                        "comment": "A reference to table ihm_cross_link_restraint.id.",
                        "markdown_name": "Restraint Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_restraint_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    {
                        "comment": "A reference to table ihm_model_list.model_id.",
                        "markdown_name": "Model Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_model_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    {
                        "comment": "A reference to table ihm_pseudo_site.id.",
                        "markdown_name": "Pseudo Site Id",
                        "source": [
                            {
                                "outbound": [
                                    "PDB",
                                    "ihm_cross_link_pseudo_site_pseudo_site_id_fkey"
                                ]
                            },
                            "RID"
                        ]
                    },
                    [
                        "PDB",
                        "ihm_cross_link_pseudo_site_cross_link_partner_fkey"
                    ]
                ]
            }
        },
        {
            "schema": "PDB",
            "table": "ihm_pseudo_site",
            "uri": "tag:isrd.isi.edu,2016:visible-foreign-keys",
            "value": {
                "detailed": [
                    [
                        "PDB",
                        "ihm_cross_link_pseudo_site_pseudo_site_id_fkey"
                    ],
                    [
                        "PDB",
                        "ihm_pseudo_site_feature_pseudo_site_id_fkey"
                    ]
                ],
                "filter": "detailed"
            }
        },
#endif
