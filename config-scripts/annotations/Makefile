all: dev_annotation_config.json staging_annotation_config.json production_annotation_config.json

dev_annotation_config.json: annotation_config.cpp
	sed -e "s/catalog_number/#99/;s/<hatrac>/hatrac\/dev/g" $< | cpp -xc++ -E -Ddev | sed -e "/^#/d" | json_pp -json_opt pretty,canonical > $@

staging_annotation_config.json: annotation_config.cpp
	sed -e "s/catalog_number/#50/;s/<hatrac>/hatrac/g" $< | cpp -xc++ -E -Dstaging | sed -e "/^#/d" | json_pp -json_opt pretty,canonical > $@

production_annotation_config.json: annotation_config.cpp
	sed -e "s/catalog_number/#1/;s/<hatrac>/hatrac/g" $< | cpp -xc++ -E -Dproduction | sed -e "/^#/d" | json_pp -json_opt pretty,canonical > $@

