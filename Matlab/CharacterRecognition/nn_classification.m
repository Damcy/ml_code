function [w_hide, w_output] = nn_classification(x_train, y_train)

total_iteration = 5000000;
err_limit = 0.001;
hide_node = 30;
learn_rate = 0.4;

[row, column] = size(x_train);

w_hide = sqrt(0.01) * randn(hide_node, column+1);
w_output = sqrt(0.01) * randn(26, hide_node+1);

x_train = [ones(row, 1), x_train];

count = 0;
max = 0;
for index_ite = 1:total_iteration
    
    temp = mod(index_ite, row) + 1;
    terminate = zeros(26,1);
    terminate(y_train(temp)+1) = 1;
    
    %计算隐层输出
    o_hide = w_hide * x_train(temp, :)';
    o_hide = sigmf(o_hide, [1, 0]);
    o_hide_add_1 = [1; o_hide];
    
    %计算最终输出
    o_output = w_output * o_hide_add_1;
    o_output = sigmf(o_output, [1, 0]);
    
    %计算误差
    delta_output = o_output .* (1 - o_output) .* (o_output - terminate);
    delta_hide = w_output(:, 2:hide_node+1)' * delta_output .* (o_hide .* (1 - o_hide));
    
    err = sum((o_output - terminate) .* (o_output - terminate));
    if(err < err_limit)
        count = count + 1;
        if count > max
            max = count;
        end
    else
        count = 0;
    end
    if(count > 1500) 
        break;
    end
    %更新权值
    w_output = w_output - learn_rate * delta_output * o_hide_add_1';
    w_hide = w_hide - learn_rate * delta_hide * x_train(temp, :);
end

end