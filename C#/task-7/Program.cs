public class Program
{
    public static async Task Main(string[] args)
    {
        Task<string> booksTask = GetBooksAsync();
        Task<string> moviesTask = GetMoviesAsync();
        Task<string> musicTask = GetMusicAsync();

        var tasks = new[] { booksTask, moviesTask, musicTask };

        try
        {
            string[] results = await Task.WhenAll(tasks);

            Console.WriteLine("All tasks completed successfully:\n");

            foreach (var result in results)
            {
                Console.WriteLine(result);
            }
        }
        catch
        {
            Console.WriteLine("One or more tasks failed:\n");

            foreach (var task in tasks)
            {
                if (task.IsCompletedSuccessfully)
                {
                    Console.WriteLine(task.Result);
                }
                else if (task.IsFaulted)
                {
                    foreach (var ex in task.Exception.InnerExceptions)
                    {
                        Console.WriteLine($"Error: {ex.Message}");
                    }
                }
            }
        }
    }

    public static async Task<string> GetBooksAsync()
    {
        await Task.Delay(2000);
        return "Books: Harry Potter, The Lord of the Rings";
    }

    public static async Task<string> GetMoviesAsync()
    {
        await Task.Delay(2000);
        return "Movies: The Shawshank Redemption, The Godfather";
    }

    public static async Task<string> GetMusicAsync()
    {
        await Task.Delay(2000);
        throw new Exception("Failed to fetch music data");
        // return "Music: ARR, Michael Jackson";
    }
}