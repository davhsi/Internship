namespace Demo.Models;

public class Person
{
    public string Name { get; init; }
    // meaning Name can only be initialized once 
    // while object creation and cannot be set again
    public int Age { get; set; } //can be both get and set

    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }

    public void Introduce()
    {
        Console.WriteLine($"Hi, I am {Name}, Age {Age}");
    }
}