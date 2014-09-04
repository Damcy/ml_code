function [err_rate] = optimization(co_y, initMatrix, outMatrix, transferMatrix, x_mark)

[row, column] = size(x_mark);

y = co_y(:, 1);

iter = 1;
while iter < row
    temp = iter+1;
    while x_mark(temp, 2) ~= -1
        temp = temp + 1;
    end
    
    for iter_temp = iter+1 : temp
        test = y(iter:iter_temp, 1);
        [probability] = probability_test(transferMatrix, initMatrix, outMatrix, test);
        if probability < 1e-5
            y(iter_temp) = co_y(iter_temp, 2);
            break;
        end
    end
    
    iter = temp + 1;
end

y_final = co_y(:, 3);

err_sum = sum(y_final ~= y);
err_rate = err_sum / row;

end