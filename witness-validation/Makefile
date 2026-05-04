OUT_DIR ?= out
GOBLINT_DIR ?=
WITNESS_INJECT ?=
CC ?= cc
ARGS ?= 1000 4

GOBLINT_ANALYZER := $(GOBLINT_DIR)/bin/goblint
GOBLINT_CONF := $(GOBLINT_DIR)/share/goblint/conf/examples/very-precise.json
WITNESS := $(OUT_DIR)/witness.yml
INJECTED_WITNESS := $(OUT_DIR)/witness.injected.yml
INJECTED_SOURCE := $(OUT_DIR)/example.injected.c
INJECTED_BIN := $(OUT_DIR)/example.injected

all:
	$(MAKE) vanilla
	$(MAKE) witness
	$(MAKE) validate
	$(MAKE) inject

clean:
	rm -rf $(OUT_DIR)

$(OUT_DIR)/example.c: example.c
	mkdir -p "$(OUT_DIR)"
	cp $< $@

witness: $(OUT_DIR)/example.c
	"$(GOBLINT_ANALYZER)" \
		--conf "$(GOBLINT_CONF)" \
		--enable witness.yaml.enabled \
		--set witness.yaml.path "$(WITNESS)" \
		$(OUT_DIR)/example.c

validate: $(OUT_DIR)/example.c
	@test -f "$(WITNESS)" || { echo "Missing $(WITNESS). Run 'make witness' first."; exit 1; }
	"$(GOBLINT_ANALYZER)" \
		--witness.yaml.unassume "$(WITNESS)" \
		--witness.yaml.validate "$(WITNESS)" \
		--conf "$(GOBLINT_CONF)" \
		$(OUT_DIR)/example.c

inject: $(OUT_DIR)/example.c
	@test -f "$(WITNESS)" || { echo "Missing $(WITNESS). Run 'make witness' first."; exit 1; }
	cp example.c "$(INJECTED_SOURCE)"
	cp "$(WITNESS)" "$(INJECTED_WITNESS)"
	sed -i "s|$(OUT_DIR)/example.c|example.injected.c|g" "$(INJECTED_WITNESS)"
	cd "$(OUT_DIR)" && "$(WITNESS_INJECT)" --witness-yaml witness.injected.yml example.injected.c
	"$(CC)" -o "$(INJECTED_BIN)" -g -O0  "$(INJECTED_SOURCE)"
	"$(INJECTED_BIN)" $(ARGS)

$(OUT_DIR)/vanilla: example.c
	mkdir -p "$(OUT_DIR)"
	"$(CC)" -o "$@" -g -O0  $<

vanilla: $(OUT_DIR)/vanilla
	$< $(ARGS)

.PHONY:	 all clean witness validate inject vanilla
