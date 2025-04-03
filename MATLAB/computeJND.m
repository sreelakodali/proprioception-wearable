function [JND, JND_abs, pse, pse_abs] = computeJND(test, ref)

% compute PSE
pse = mean(test(end-4:end));
JND = abs(ref - pse);
JND_abs = mean(abs(ref - test(end-4:end)));

if (pse < ref)
    pse_abs = ref - JND_abs;
else
    pse_abs =  ref + JND_abs;
end

end