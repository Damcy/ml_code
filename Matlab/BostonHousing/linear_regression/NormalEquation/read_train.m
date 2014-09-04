function [x, y] = read_train()

data = load('housing_train.txt');

x = data(:, 1:13);
y = data(:, 14);

end