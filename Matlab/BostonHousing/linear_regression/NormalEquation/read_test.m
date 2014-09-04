function [x, y] = read_test()

data = load('housing_test.txt');

x = data(:, 1:13);
y = data(:, 14);

end