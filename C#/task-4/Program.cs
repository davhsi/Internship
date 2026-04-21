using Task4.Models;

public class Program
{
    public static void Main(string[] args)
    {
        List<Student> students = new List<Student>();

        var s1 = new Student("Davish", 22, 7.9);
        var s2 = new Student("Vignesh", 23, 8.2);
        var s3 = new Student("Suseeth", 20, 9.4);
        var s4 = new Student("Rohit", 24, 7.8);

        students.Add(s1);
        students.Add(s2);
        students.Add(s3);
        students.Add(s4);

        var filteredStudents = students.Where(s => s.Grade > 8);
        var sortedStudents = filteredStudents.OrderBy(s => s.Name);

        Console.WriteLine("Students with Grade above 8 and sorted by name");

        foreach(var s in sortedStudents){
            Console.WriteLine($"Name: {s.Name}, Grade: {s.Grade}, Age: {s.Age}");
        }
    }
}