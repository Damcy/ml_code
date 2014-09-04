function [theta] = LR_learn(x, y)

[row, column] = size(x); 
iter_total = 10000;
alpha = 0.001;

x = [ones(row, 1), x];

%��ʼ��theta��ȫ0
theta = zeros(column+1, 1);
J = zeros(iter_total, 1);

%����
for iter_index = 1:iter_total
    err = x*theta - y;
    J(iter_index) = err' * err / (2*row);
    gradient = (x' * err) / row;
    if(sum(alpha *gradient(:,1) > 0.0001) == 0)
        break;      %ÿһ��ı仯С��0.0001
    end
    theta = theta - alpha * gradient;
end

plot(J);

end