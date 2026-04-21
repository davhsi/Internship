public class ScoreCounter
{
    private int _count = 0;
    private int _threshold;
    // event named OnThresholdReached based on the delegate type ThresholdReachedHandler
    public event ThresholdReachedHandler? OnThresholdReached;
    public ScoreCounter(int threshold)
    {
        _threshold = threshold;
    }
    public void Increment()
    {
        _count++;
        Console.WriteLine($"Counter: {_count}");
        if(_count == _threshold)
        {
            // invoke the event - this will call all the methods subscribed to it
            OnThresholdReached?.Invoke(_count);
        }
    }
}