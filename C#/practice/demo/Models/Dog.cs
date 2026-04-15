namespace Demo.Models;

public class Dog : Animal // Dog inherits Animal
{
    public Dog(string name) : base(name) { } //using parent class constructor

    public override void Speak()
    {
        Console.WriteLine($"{Name} barks!!");
    }
}