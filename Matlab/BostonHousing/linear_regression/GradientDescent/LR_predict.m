function [y] = LR_predict(x, w)

[row, column] = size(x);

x = [ones(row, 1), x];

y = x * w;


end
