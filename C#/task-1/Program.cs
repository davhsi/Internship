class Program
{
    public static void Main(string[] args)
    {
        var input = Console.ReadLine();
        if (int.TryParse(input, out int i))
        {
            if (i < 0)
            {
                Console.WriteLine("Try a positive number");
                return;
            }

            try
            {
                long result = Factorial(i);
                Console.WriteLine($"Factorial of {i} = {result}");
            }
            catch (OverflowException)
            {
                Console.WriteLine("Try a smaller number");
            }
        }
        else
        {
            Console.WriteLine("Invalid Input");
        }
    }

    static long Factorial(int n)
    {
        if (n == 0 || n == 1)
            return 1;

        return checked(n * Factorial(n - 1));
    }
}