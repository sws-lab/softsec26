OUT_DIR ?= out
GOBLINT_DIR ?=
WITNESS_INJECT ?=
CC ?= cc
ARGS ?= 1000 4

GOBLINT_ANALYZER := $(GOBLINT_DIR)/bin/goblint
GOBLINT_CONF := $(GOBLINT_DIR)/share/goblint/conf/examples/very-precise.json

all: vanilla validate inject

clean:
	rm -rf $(OUT_DIR)

$(OUT_DIR)/example.c: example.c
	mkdir -p "$(OUT_DIR)"
	cp $< $@

$(OUT_DIR)/witness.yml: $(OUT_DIR)/example.c
	"$(GOBLINT_ANALYZER)" \
		--conf "$(GOBLINT_CONF)" \
		--enable witness.yaml.enabled \
		--set witness.yaml.path "$@" \
		$(OUT_DIR)/example.c

validate: $(OUT_DIR)/witness.yml
	"$(GOBLINT_ANALYZER)" \
		--witness.yaml.unassume $< \
		--witness.yaml.validate $< \
		--conf "$(GOBLINT_CONF)" \
		$(OUT_DIR)/example.c

$(OUT_DIR)/example.injected: $(OUT_DIR)/witness.yml
	cp example.c "$(OUT_DIR)/example.injected.c"
	cp "$(OUT_DIR)/witness.yml" "$(OUT_DIR)/witness.injected.yml"
	sed -i "s|out/example.c|example.injected.c|g" "$(OUT_DIR)/witness.injected.yml"
	cd "$(OUT_DIR)" && "$(WITNESS_INJECT)" --witness-yaml witness.injected.yml example.injected.c
	"$(CC)" -o "$@" -g -O0  "$(OUT_DIR)/example.injected.c"

$(OUT_DIR)/vanilla: example.c
	mkdir -p "$(OUT_DIR)"
	"$(CC)" -o "$@" -g -O0  $<

inject: $(OUT_DIR)/example.injected
	$< $(ARGS)

vanilla: $(OUT_DIR)/vanilla
	$< $(ARGS)

.PHONY:	 all clean validate inject