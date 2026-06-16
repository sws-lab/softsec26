package average;

import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.junit.FuzzTest;

class AverageDiffFuzzTest {

    @FuzzTest(maxDuration = "30s")
    void agree(FuzzedDataProvider data) {
        int a = data.consumeInt();
        int b = data.consumeInt();
        int r1 = Average.average1(a, b);
        int r2 = Average.average2(a, b);
        if (r1 != r2) {
            throw new AssertionError("disagreement: average1(" + a + ", " + b
                + ") = " + r1 + " but average2(" + a + ", " + b + ") = " + r2);
        }
    }
}
