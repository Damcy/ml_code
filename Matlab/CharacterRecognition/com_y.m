function [co_y, err_rate, outMatrix] = com_y(y_predict, y_test)

[row, column] = size(y_predict);
% outMatrix = zeros(26, 26);

co_y = [y_predict, y_test];

total = sum(y_predict(:, 1) ~= y_test);
err_rate = total / row;
outMatrix = zeros(26,26);
for iter = 1:row
    outMatrix(co_y(iter,2)+1, co_y(iter,1)+1) = outMatrix(co_y(iter,2)+1, co_y(iter,1)+1) + 1;
end
% 
for iter = 1:26
    row_sum = sum(outMatrix(iter,:));
    outMatrix(iter,:) = outMatrix(iter,:) ./ row_sum;
end
end