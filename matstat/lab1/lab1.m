function lab1()
    clear all;
    X = csvread('data.csv');
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
    
    m = getNumberOfSubintervals(X);
    fprintf('m = %s\n', num2str(m))
    
    
    createGroup(X);
    hold on;
    f(X, MU, Ssqr, m);

    figure;
    empiricF(X);
    hold on;
    F(X, MU, Ssqr, m);
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

function m = getNumberOfSubintervals(X)
    m = floor(log2(length(X)) + 2);
end

function createGroup(X)
    n = length(X);
    m = getNumberOfSubintervals(X);
    
    Table1 = zeros(1, m+1);
    Table2 = zeros(1, m+1);
    Delta = (max(X) - min(X)) / m;
    fprintf('Delta = %s\n', num2str(Delta));
    
    for i = 0: m
        Table1(i+1) = X(1) + Delta * i;
    end
    
    j = 1;
    count = 0;
    for i = 1:n
        if (X(i) >= Table1(j+1)) 
            j = j + 1; 
        end
        Table2(j) = Table2(j) + 1;
        count = count + 1;
    end
    disp(Table1);
    disp(sum(Table2))
    
    
    for i = 1:m-1
        fprintf('[%5.2f; %5.2f) ', Table1 (i), Table1(i+1));
    end 
    fprintf('[%5.2f, %5.2f]\n', Table1(m), Table1(m+1));
    
    for i = 1:m 
        fprintf('%8d       ', Table2(i));
    end
    fprintf('\n\n');

	Xbuf = Table2(1:m+1);
    for i = 1:m+1
        Xbuf(i) = Table2(i) / (n*Delta); 
    end
    
    stairs(Table1, Xbuf),grid;
end

function f(X, MX, DX, m)
    R = X(end) - X(1);
    delta = R/m;
    Sigma = sqrt(DX);
    
    Xn = (MX - R): delta/50 :(MX + R);
    Y = normpdf(Xn, MX, Sigma);
    plot(Xn, Y), grid;
end

function F(X, MX, DX, m)
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
