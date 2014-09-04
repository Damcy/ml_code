function [err_rate] = viterbi(co_y, initMatrix, outMatrix, transferMatrix, x_mark)

[row, column] = size(x_mark);

y = co_y(:, 1);

iter = 1;
while iter < row
    temp = iter+1;
    while x_mark(temp, 2) ~= -1
        temp = temp + 1;
    end
    
    test = y(iter:temp, 1)+1;
    
    top = temp-iter+1;
    fai = zeros(26, top);
    delta = zeros(26, top);
    
    delta(:, 1) = initMatrix' .* outMatrix(:, test(1));
    
    for i = 2 : top
        for j = 1 : 26
            for k = 1 : 26
                times = delta(k, i-1) * transferMatrix(k, j) * outMatrix(j, test(i));
                if times > delta(j, i)
                    delta(j, i) = times;
                    fai(j, i) = k;
                end
            end
        end
    end
    
    [value, pos] = max(delta(:, top));
    temp_list = zeros(top, 1);
    iter_2 = top;
    while iter_2 > 0
        temp_list(iter_2) = pos-1;
        pos = fai(pos, iter_2);
        iter_2 = iter_2 - 1;
    end

    y(iter:temp, 1) = temp_list;
    
    iter = temp + 1;
end

y_final = co_y(:, 2);

err_sum = sum(y_final ~= y);
err_rate = err_sum / row;

end