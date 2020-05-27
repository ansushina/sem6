function lab2()
    X = [14.90, 14.40, 13.56, 15.55, 13.97, 16.33, 14.37, 13.46, 15.51, 14.69,...
         13.41, 14.24, 15.65, 14.54, 13.55, 13.15, 14.32, 15.04, 13.27, 14.60,...
         13.83, 13.93, 14.11, 14.15, 15.48, 15.96, 14.46, 13.87, 13.67, 15.30, ...
         13.95, 16.08, 18.25, 14.93, 15.37, 14.38, 15.56, 13.92, 14.23, 12.80, ...
         13.16, 13.89, 14.24, 13.90, 12.82, 13.20, 13.89, 13.50, 13.44, 16.13, ...
         14.68, 15.27, 13.35, 13.62, 16.16, 16.46, 13.83, 14.13, 15.68, 15.22, ...
         12.59, 12.94, 13.09, 16.54, 14.61, 14.63, 14.17, 13.34, 16.74, 16.30, ...
         13.74, 15.02, 14.96, 15.87, 16.03, 12.87, 14.32, 14.48, 14.57, 14.43, ...
         12.61, 14.52, 15.29, 12.07, 14.58, 11.74, 14.97, 14.31, 12.94, 12.82, ...
         14.13, 14.48, 12.25, 14.39, 15.08, 12.87, 14.25, 15.12, 15.35, 12.27, ...
         14.43, 13.85, 13.16, 16.77, 14.47, 14.89, 14.95, 14.55, 12.80, 15.26, ...
         13.32, 14.92, 13.44, 13.48, 12.81, 15.01, 13.19, 14.68, 14.44, 14.89]; 
     
    N = 1:length(X);
    
    gamma = 0.9;
    alpha = (1 - gamma)/2;

    mu = expectation(X);
    sSqr = variance(X); 

    fprintf('mu = %.2f\n', mu); 
    fprintf('S^2 = %.2f\n\n', sSqr);

    muArray = expectationArray(X, N);
    varArray = varianceArray(X, N);
 
    figure
    plot([N(1), N(end)], [mu, mu], 'm');
    hold on;
    plot(N, muArray, 'g');
    
    Ml = muArray - sqrt(varArray./N).*tinv(1 - alpha, N - 1);
    plot(N, Ml, 'b');

    fprintf('mu_low = %.2f\n', Ml(end));
    
    Mh = muArray + sqrt(varArray./N).*tinv(1 - alpha, N - 1);
    plot(N, Mh, 'r'), legend('y=mu', 'y=mu_n', 'y=mu-low_n', 'y=mu-high_n');
    grid on;
    hold off;
    
    fprintf('mu_high = %.2f\n', Mh(end));

    figure
    plot([N(1), N(end)], [sSqr, sSqr], 'm');
    hold on;
    plot(N, varArray, 'g');
    
    Sl = varArray.*(N - 1)./chi2inv(1 - alpha, N - 1);
    plot(N, Sl, 'b');
    
    Sh = varArray.*(N - 1)./chi2inv(alpha, N - 1);
    plot(N, Sh, 'r'), legend('z=S^2', 'z=S^2_n', 'z=S^2-low_n', 'z=S^2-high_n');
    grid on;
    hold off;


    fprintf('sigma^2_low = %.2f\n', Sl(end));
    fprintf('sigma^2_high = %.2f\n', Sh(end));
end

function mu = expectation(X)
   mu = mean(X);
end

function sSqr = variance(X)
    sSqr = var(X);
end

function muArray = expectationArray(X, N)
    muArray = zeros(1, length(N));
    for i = 1:length(N)
        muArray(i) = expectation(X(1:N(i)));
    end
end

function varArray = varianceArray(X, N)
    varArray = zeros(1, length(N));
    for i = 1:length(N)
        varArray(i) = variance(X(1:N(i)));
    end
end
