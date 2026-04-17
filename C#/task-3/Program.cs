public class Program
{
    public static void Main(string[] args)
    {
        List<string> tasks = [];

        Console.WriteLine("DAV Task Manager");

        while (true)
        {
            Console.WriteLine("\nOptions: ADD | REMOVE | DISPLAY | EXIT");
            Console.Write("Enter option: ");

            string input = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(input))
            {
                Console.WriteLine("No input detected. Please try again.");
                continue;
            }

            string option = input.Trim().ToUpper();

            switch (option)
            {
                case "ADD":
                    Console.Write("Enter task to add: ");
                    string newTask = Console.ReadLine();

                    if (string.IsNullOrWhiteSpace(newTask))
                    {
                        Console.WriteLine("Task cannot be empty.");
                    }
                    else
                    {
                        newTask = newTask.Trim();
                        tasks.Add(newTask);
                        Console.WriteLine($"Task \"{newTask}\" added.");
                    }
                    break;

                case "REMOVE":
                    if (tasks.Count == 0)
                    {
                        Console.WriteLine("No tasks to remove.");
                        break;
                    }

                    Console.Write("\nEnter task number to remove: ");
                    string indexInput = Console.ReadLine();

                    if (!int.TryParse(indexInput, out int taskNumber))
                    {
                        Console.WriteLine("Invalid input. Please enter a number.");
                        break;
                    }

                    if (taskNumber < 1 || taskNumber > tasks.Count)
                    {
                        Console.WriteLine($"Invalid number. Enter between 1 and {tasks.Count}.");
                        break;
                    }

                    string removedTask = tasks[taskNumber - 1];
                    tasks.RemoveAt(taskNumber - 1);
                    Console.WriteLine($"Task \"{removedTask}\" removed.");
                    break;

                case "DISPLAY":
                    if (tasks.Count == 0)
                    {
                        Console.WriteLine("No tasks available.");
                    }
                    else
                    {
                        Console.WriteLine("\n--- Your Tasks ---");
                        for (int i = 0; i < tasks.Count; i++)
                        {
                            Console.WriteLine($"{i + 1}. {tasks[i]}");
                        }
                    }
                    break;

                case "EXIT":
                    Console.WriteLine("Thank You");
                    return;

                default:
                    Console.WriteLine("Invalid option. Please type ADD, REMOVE, DISPLAY, or EXIT.");
                    break;
            }
        }
    }
}