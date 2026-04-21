public class ScoreNotifier
{
    // matches delegate signature
    public void LogToConsole(int count)
    {
        Console.WriteLine($"[Logger] Threshold reached at count: {count}");
    }
    public void SendAlert(int count)
    {
        Console.WriteLine($"[ALERT] Counter hit {count}. Sending mail .....");
    }
}
