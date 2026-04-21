public class InMemoryRepository<T> : IRepository<T> where T : class, IEntity
{
    private readonly List<T> _items = new List<T>();

    public void Add(T item)
    {
        _items.Add(item);
    }

    public List<T> GetAll()
    {
        return _items;
    }

    public T GetById(int id)
    {
        return _items.FirstOrDefault(x => x.Id == id);
    }

    public void Update(T item)
    {
        var existing = GetById(item.Id);
        if (existing != null)
        {
            _items.Remove(existing);
            _items.Add(item);
        }
    }

    public void Delete(int id)
    {
        var item = GetById(id);
        if (item != null)
        {
            _items.Remove(item);
        }
    }
}