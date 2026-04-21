public interface IRepository<T> where T : IEntity
{
    void Add(T item);
    List<T> GetAll();
    T GetById(int id);
    void Update(T item);
    void Delete(int id);
}