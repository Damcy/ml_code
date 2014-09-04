function [probability] = probability_test(transferMatrix, initMatrix, outMatrix, test)

[row, column] = size(test);

proMatrix = zeros(26, row);

proMatrix(:, 1) = initMatrix' .* outMatrix(:, test(1)+1);

for iter = 2 : row
    for iter_i = 1 : 26
        proMatrix(iter_i, iter) = outMatrix(iter_i, test(iter)+1) * sum(proMatrix(:, iter-1) .* transferMatrix(:, iter_i));
    end
end

probability = sum(proMatrix(:, row));

end