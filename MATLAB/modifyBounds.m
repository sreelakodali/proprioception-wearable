function [peaks] = modifyBounds(peaks, lr, lf, rr, rf)

    if (~isempty(lr))
        peaks(lr,1) =  peaks(lr,1) + 1;
    end
    
    if (~isempty(lf))
        peaks(lf,2) =  peaks(lf,2) + 1;
    end
    
    if (~isempty(rr))
        peaks(rr,3) =  peaks(rr,3) + 1;
    end

    if (~isempty(rf))
        peaks(rf,4) =  peaks(rf,4) + 1;
    end
end