namespace Demo.Models;

public interface IDrawable
{
    void Draw();
}

public class Circle : Shape, IDrawable
{
    public double Radius { get; set; }

    public Circle(double radius)
    {
        Radius = radius;
    }

    public override double Area()
    {
        return Math.PI * Radius * Radius;
    }

    public void Draw() // implementing the interface method
    {
        Console.WriteLine("Drawing circle");
    }

}