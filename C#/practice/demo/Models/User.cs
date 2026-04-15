namespace Demo.Models;

public record User(string Name, int Age);

// record is a special type of class designed for immutable data and value-based comparison
// 1. Immutable by default
// 2. Value-based equality
// 3. Works with with