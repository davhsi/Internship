using Demo.Models;
using Demo.Services;

class Program
{
    static void Main(string[] args)
    {
        var person = new Person("Davish", 22);
        person.Introduce();
        person.Age = 23;
        // person.Name = "Davish E" -> error because init = final


        Animal animal = new Animal("Generic");
        animal.Speak();

        Animal dog = new Dog("Laika");
        dog.Speak();

        Circle circle = new Circle(5);
        Console.WriteLine($"Area: {circle.Area()}");
        circle.Draw();

        var user1 = new User("Davish", 22);
        var user2 = user1 with { Age = 23 };

        Console.WriteLine(user1);
        Console.WriteLine(user2);

        var mathService = new MathService();

        int sum = mathService.Compute(2, 3, (a, b) => a + b);
        int product = mathService.Compute(2, 3, (a, b) => a * b);

        Console.WriteLine($"Sum: {sum}");
        Console.WriteLine($"Product: {product}");
    }
}