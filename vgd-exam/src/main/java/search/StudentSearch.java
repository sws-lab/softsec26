package search;

// Binary search over a sorted (ascending) int array. The spec for Part D asks
// for the index of the FIRST occurrence of key (the leftmost one), or -1 if key
// does not occur.
//
// This is the implementation under test in Part D. It is the textbook binary
// search everyone writes: it returns as soon as it lands on a matching element.
// On an array with no repeats that element is the only one, so it is always
// right -- it "obviously works" on every example you try by hand. The bug only
// shows when key occurs more than once: the search can stop on a later copy and
// return that index instead of the first. This is the kind of bug that survives
// code review precisely because casual testing never repeats a value.
public final class StudentSearch {
    private StudentSearch() {}

    public static int find(int[] a, int key) {
        int lo = 0;
        int hi = a.length - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (a[mid] == key) {
                return mid;          // first match the search happens to hit -- not always the leftmost
            }
            if (a[mid] < key) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return -1;
    }

    // A few interesting inputs to look at by hand: `make demo-search`.
    public static void main(String[] args) {
        System.out.println("find({1,3,5,7,9}, 7) = " + find(new int[] {1, 3, 5, 7, 9}, 7));
        System.out.println("find({1,2,2,2,3}, 2) = " + find(new int[] {1, 2, 2, 2, 3}, 2));
        System.out.println("find({1,2,2,2,3}, 4) = " + find(new int[] {1, 2, 2, 2, 3}, 4));
    }
}
