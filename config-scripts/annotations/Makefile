all: dev_annotation_config.json staging_annotation_config.json production_annotation_config.json

dev_annotation_config.json: annotation_config.cpp
	cpp -E -Ddev $< | sed -e "/^#/d" | json_pp -json_opt pretty,canonical > $@

staging_annotation_config.json: annotation_config.cpp
	cpp -E -Dstaging $< | sed -e "/^#/d" | json_pp -json_opt pretty,canonical > $@

production_annotation_config.json: annotation_config.cpp
	cpp -E -Dproduction $< | sed -e "/^#/d" | json_pp -json_opt pretty,canonical > $@

