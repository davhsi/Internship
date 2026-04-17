using Task2.Models;

public class Program
{
    public static void Main(string[] args)
    {
        var person1 = new Person("Davish", 22);
        var person2 = new Person("Vignesh", 21);
        var person3 = new Person("Kishore", 10);

        person1.Introduce();
        person2.Introduce();
        person3.Introduce();
    }
}