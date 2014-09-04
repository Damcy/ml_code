function [x_train, y_train, x_test, y_test, x_mark] = read_data()

train_data = load('train1.txt');
test_data = load('test1.txt');

x_train = train_data(:, 2:129);
y_train = train_data(:, 1);

x_test = test_data(:, 2:129);
y_test = test_data(:, 1);

x_mark = load('testMark1.txt');

% x = load('matrix.txt');
% y = load('mark.txt');

end