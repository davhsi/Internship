namespace Demo.Models;

public class Animal
{
    public string Name { get; init; }
    public Animal(string name)
    {
        Name = name;
    }

    public virtual void Speak()
    {
        Console.WriteLine("AAAAAHHHH!!");
    }
}
