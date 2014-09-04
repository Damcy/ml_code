function [w] = LR_learn(x, y)

[row, column] = size(x); 

x_0 = ones(row, 1);

x_fix = [x_0, x];

w = pinv(x_fix' * x_fix) * x_fix' * y;

end