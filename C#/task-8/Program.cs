class Program
{
    static void Main()
    {
        IRepository<Product> repo = new InMemoryRepository<Product>();

        repo.Add(new Product { Id = 1, Name = "Macbook", Price = 200000 });
        repo.Add(new Product { Id = 2, Name = "Smartphone", Price = 25000 });

        foreach (var p in repo.GetAll())
        {
            Console.WriteLine($"{p.Id} - {p.Name} - {p.Price}");
        }
    }
}