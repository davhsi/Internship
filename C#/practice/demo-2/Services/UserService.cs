using Demo2.Models;

using Demo2.Data;

namespace Demo2.Services;

public class UserService
{
    private readonly FakeDatabase _db;

    public UserService(FakeDatabase db)
    {
        _db = db;
    }

    public async Task<List<User>> GetAdultsAsync()
    {
        var users = await _db.GetUsersAsync();

        return users.Where(u => u.Age >= 18).OrderBy(u => u.Name).ToList();
    }

    public async Task<User?> GetByIdAsync(int id)
    {
        var users = await _db.GetUsersAsync();
        return users.FirstOrDefault(u => u.Id == id);
    }
}