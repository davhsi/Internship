namespace Task2.Models;

public class Person
{
    public string Name { get; set; }

    public int Age { get; set; }

    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }

    public void Introduce()
    {
        Console.WriteLine($"Hi I am {Name} and I am {Age} years old");
    }

}
