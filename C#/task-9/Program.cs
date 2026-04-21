using System.Reflection;

// Define a custom attribute [Runnable] that can be applied to methods.
[AttributeUsage(AttributeTargets.Method)]
public class RunnableAttribute : Attribute
{
}

public class Tasks
{
    [Runnable]
    public void Task1()
    {
        Console.WriteLine("Task1 executed");
    }

    [Runnable]
    public void Task2()
    {
        Console.WriteLine("Task2 executed");
    }

    public void Task3()
    {
        Console.WriteLine("This method should not be executed");
    }
}

public class MoreTasks
{
    [Runnable]
    public void Task4()
    {
        Console.WriteLine("Task4 executed");
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        // Get current assembly
        // Assembly is a class in the System.Reflection namespace that represents a .NET assembly,
        // which is a compiled code library used for deployment, versioning, and security.
        // It contains metadata about the types defined in the assembly, as well as the code itself.
        var assembly = Assembly.GetExecutingAssembly();

        // here we are using reflection to get all types and methods in the assembly,
        // and check if they have the [Runnable] attribute.
        foreach (var type in assembly.GetTypes())
        {
            foreach (var method in type.GetMethods())
            {
                // Check if method has [Runnable]
                if (method.GetCustomAttribute(typeof(RunnableAttribute)) != null)
                {
                    // Create instance of class
                    var instance = Activator.CreateInstance(type);

                    // Invoke method
                    method.Invoke(instance, null);
                }
            }
        }
    }
}