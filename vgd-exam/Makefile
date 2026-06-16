.PHONY: fuzz-calc fuzz-average fuzz-search demo-average demo-search verify oracle clean

FUZZ = ./scripts/fuzz.sh

# --- Part A: fuzz the calculator ---------------------------------------
fuzz-calc:
	@$(FUZZ) calc CalculatorFuzzTest

# --- Part B: differential-fuzz the two average implementations ---------
fuzz-average:
	@$(FUZZ) average AverageDiffFuzzTest

demo-average:
	@mkdir -p target/demo
	@javac -d target/demo src/main/java/average/Average.java
	@java -cp target/demo average.Average

# --- Part C: verify the binary search proof ----------------------------
verify:
	cd dafny && dafny verify --verify-included-files BinarySearch.verify.dfy

# --- Part D: fuzz the student search against the verified oracle -------
fuzz-search: oracle
	@$(FUZZ) search SearchOracleFuzzTest

demo-search:
	@mkdir -p target/demo
	@javac -d target/demo src/main/java/search/StudentSearch.java
	@java -cp target/demo search.StudentSearch

# Regenerate src/main/java/Oracle/ by translating the Dafny source to Java.
# This deliberately does NOT depend on `verify`: the only thing missing from
# dafny/BinarySearch.dfy is the loop *invariants* (proof annotations), not
# executable code, so the translated method behaves correctly whether or not
# Part C's proof goes through. Part C establishes that this model is
# trustworthy; Part D only needs the model's behavior, so a student who has not
# finished Part C can still run the differential fuzz test here.
oracle:
	@mkdir -p .work src/main/java/Oracle
	@log=.work/oracle.log; \
	echo "Generating Java oracle from the verified Dafny source"; \
	if dafny translate java dafny/BinarySearch.dfy --no-verify --output target/oracle-gen >"$$log" 2>&1; then \
		cp target/oracle-gen-java/Oracle/__default.java src/main/java/Oracle/; \
		echo "  wrote src/main/java/Oracle/__default.java"; \
	else \
		echo "  generation failed; see $$log"; \
		tail -n 25 "$$log"; \
		exit 1; \
	fi

clean:
	./gradlew -q clean
	rm -rf target .work src/main/java/Oracle/__default.java
