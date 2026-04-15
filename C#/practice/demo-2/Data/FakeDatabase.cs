using Demo2.Models;

namespace Demo2.Data;

public class FakeDatabase
{
    private List<User> _users = new()
    {
        new User(1, "Davish", 22),
        new User(2, "User2", 12),
        new User(3, "User3", 31),
        new User(4, "User4", 10)
    };

    public async Task<List<User>> GetUsersAsync()
    // Task Represents an asynchronous operation that can return a value.
    {
        await Task.Delay(500);
        return _users;
    }
}