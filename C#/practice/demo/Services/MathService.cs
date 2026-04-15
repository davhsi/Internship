namespace Demo.Services;

public class MathService
{
    public int Compute(int a, int b, Func<int, int, int> operation)
    {
        return operation(a, b);
    }
}