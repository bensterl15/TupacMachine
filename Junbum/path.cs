using System;
namespace HelloWorld
{
    class Hello 
    {
        static void Main() 
        {
            Console.WriteLine(System.IO.Directory.GetCurrentDirectory());
            string path = System.AppDomain.CurrentDomain.BaseDirectory;
            string newPath = path + "script.py";
            Console.WriteLine(newPath);
            string[] lines = System.IO.File.ReadAllLines(newPath);

            // Display the file contents by using a foreach loop.
            System.Console.WriteLine("Contents of script.py = ");
            foreach (string line in lines)
            {
                // Use a tab to indent each line of the file.
                Console.WriteLine("\t" + line);
            }
            // Keep the console window open in debug mode.
            Console.WriteLine("Press any key to exit.");
            Console.ReadKey();
        }
    }
}