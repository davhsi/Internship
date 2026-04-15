using Demo2.Services;
using Demo2.Data;
namespace Demo2;

class Program
{
    static async Task Main(string[] args)
    {
        var database = new FakeDatabase();
        var userService = new UserService(database);

        var adults = await userService.GetAdultsAsync();

        Console.WriteLine("Adult Users:");
        foreach (var user in adults)
        {
            Console.WriteLine(user);
        }

        Console.WriteLine();

        var userById = await userService.GetByIdAsync(2);

        Console.WriteLine("User with ID 2:");
        if (userById is null)
        {
            Console.WriteLine("Not found");
        }
        else
        {
            Console.WriteLine(userById);
        }
    }
}