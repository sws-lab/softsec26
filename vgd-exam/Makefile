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

# Regenerate src/main/java/Oracle/ from the Dafny source. Verification runs
# first, so this only succeeds once the proof in dafny/BinarySearch.dfy is
# complete.
oracle: verify
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
