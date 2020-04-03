function lab1()
    clear all;
    X = [14.90,14.40,13.56,15.55,13.97,16.33,14.37,13.46,15.51,14.69,13.41,14.24,15.65,14.54,13.55,13.15,14.32,15.04,13.27,14.60,13.83,13.93,14.11,14.15,15.48,15.96,14.46,13.87,13.67,15.30,13.95,16.08,18.25,14.93,15.37,14.38,15.56,13.92,14.23,12.80,13.16,13.89,14.24,13.90,12.82,13.20,13.89,13.50,13.44,16.13,14.68,15.27,13.35,13.62,16.16,16.46,13.83,14.13,15.68,15.22,12.59,12.94,13.09,16.54,14.61,14.63,14.17,13.34,16.74,16.30,13.74,15.02,14.96,15.87,16.03,12.87,14.32,14.48,14.57,14.43,12.61,14.52,15.29,12.07,14.58,11.74,14.97,14.31,12.94,12.82,14.13,14.48,12.25,14.39,15.08,12.87,14.25,15.12,15.35,12.27,14.43,13.85,13.16,16.77,14.47,14.89,14.95,14.55,12.80,15.26,13.32,14.92,13.44,13.48,12.81,15.01,13.19,14.68,14.44,14.89];
    X = sort(X);
    
    Mmax = max(X);
    Mmin = min(X);
    
    fprintf('Mmin = %s\n', num2str(Mmin));
    fprintf('Mmax = %s\n', num2str(Mmax));
    
    R = Mmax - Mmin;
    fprintf('R = %s\n', num2str(R));
    
    MU = getMU(X);
    fprintf('MU = %s\n', num2str(MU));
    
    Ssqr = getSsqr(X);
    fprintf('S^2 = %s\n', num2str(Ssqr));
    
    m = getNumberOfIntervals(X);
    fprintf('m = %s\n', num2str(m))
    
    createGroup(X);
    hold on;
    distributionDensity(X, MU, Ssqr, m);

    figure;
    empiricF(X);
    hold on;
    distribution(X, MU, Ssqr, m);
end

function mu = getMU(X)
    n = length(X);
    mu = sum(X)/n;
end

function Ssqr = getSsqr(X)
    n = length(X);
    MX = getMU(X);
    Ssqr = sum((X - MX).^2) / (n-1);
end

function m = getNumberOfIntervals(X)
    m = floor(log2(length(X)) + 2);
end

function createGroup(X)
    n = length(X);
    m = getNumberOfIntervals(X);
    
    intervals = zeros(1, m+1);
    numCount = zeros(1, m+1);
    Delta = (max(X) - min(X)) / m;
    fprintf('Delta = %s\n', num2str(Delta));
    
    for i = 0: m
        intervals(i+1) = X(1) + Delta * i;
    end
    
    j = 1;
    count = 0;
    for i = 1:n
        if (X(i) >= intervals(j+1)) 
            j = j + 1; 
        end
        numCount(j) = numCount(j) + 1;
        count = count + 1;
    end
    
    for i = 1:m-1
        fprintf('[%5.2f; %5.2f) ', intervals (i), intervals(i+1));
    end 
    fprintf('[%5.2f, %5.2f]\n', intervals(m), intervals(m+1));
    
    for i = 1:m 
        fprintf('%8d       ', numCount(i));
    end
    fprintf('\n\n');

	graphBuf = numCount(1:m+1);
    for i = 1:m+1
        graphBuf(i) = numCount(i) / (n*Delta); 
    end
    
    stairs(intervals, graphBuf),grid;
end

function distributionDensity(X, MX, DX, m)
    R = X(end) - X(1);
    delta = R/m;
    Sigma = sqrt(DX);
    
    Xn = (MX - R): delta/50 :(MX + R);
    Y = normpdf(Xn, MX, Sigma);
    plot(Xn, Y), grid;
end

function distribution(X, MX, DX, m)
    R = X(end) - X(1);
    delta = R/m;
    
    Xn = (MX - R): delta :(MX + R);
    Y = 1/2 * (1 + erf((Xn - MX) / sqrt(2*DX))); 
    plot(Xn, Y, 'r'), grid;
end

function empiricF(X)  
    [yy, xx] = ecdf(X);
    
    stairs(xx, yy), grid;
end
