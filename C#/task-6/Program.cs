public class Program
{
    public static void Main(string[] args)
    {
        ScoreCounter counter = new ScoreCounter(threshold: 5);
        ScoreNotifier notifier = new ScoreNotifier();
        // subscribe methods to the event
        counter.OnThresholdReached += notifier.LogToConsole;
        counter.OnThresholdReached += notifier.SendAlert;
        counter.OnThresholdReached += (count) =>
        {
            Console.WriteLine($"[Lambda] Tiggered at {count}");

        };

        for(int i = 0; i<10; i++)
        {
            counter.Increment();
        }

    }
}