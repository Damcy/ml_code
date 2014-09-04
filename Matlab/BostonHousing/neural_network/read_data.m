function [x_train, y_train, x_test, y_test] = read_data()

data = load('housing_train.txt');

x_train = data(:, 1:13);
y_train = data(:, 14);

[row_train, column_train] = size(x_train);
% 
max_x_train = max(x_train);
min_x_train = min(x_train);
mean_x_train = mean(x_train);
std_x_train = std(x_train);

max_train = max(y_train);
min_train = min(y_train);


for index = 1:row_train
%     x_train(index, :) = (x_train(index, :) - min_x_train) ./ (max_x_train - min_x_train);
    x_train(index, :) = (x_train(index, :) - mean_x_train) ./ std_x_train;
end
%¹éÒ»»¯
y_train = (y_train - min_train) ./ (max_train - min_train);

data = load('housing_test.txt');

x_test = data(:, 1:13);
y_test = data(:, 14);
[row_test, column_test] = size(x_test);
for index = 1:row_test
%     x_test(index, :) = (x_test(index, :) - min_x_train) ./ (max_x_train - min_x_train);
    x_test(index, :) = (x_test(index, :) - mean_x_train) ./ std_x_train;
end
% 
y_test = (y_test - min_train) ./ (max_train - min_train);

end