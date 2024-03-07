function [] = plotSK(x, y, err, color, marker, sz, j, lw1, lw2, f, sc, cmap)
    xi = [x(1)-j:1:x(end)+j];
%     if f==1
%         y = flip(y);
%     end

    % error bars
    if marker == 0
        e = errorbar(x,y,err,"o"); hold on;
    elseif marker == 1
        e = errorbar(x,y,err,"s"); hold on;
    end

     % spline
%     if f==1
%         vid=interp1(x,flip(y),xi,'spline');
%     else
%         vid=interp1(x,y,xi,'spline');
%     end
%     if f==1
%         vid = flip(vid);
%     end
%    p2 = plot(xi,vid, ':'); hold on;
    %p2 = plot(x,y, ':'); hold on; % this was for worldhaptics23
     if f==1
        p2 = plot(x,y,'o');
     else 
        p2 = plot(x,y);
     end
    
    e.Color = color;
    e.LineWidth = lw1;
    
    p2.LineWidth = lw2;
    p2.Color = color;

      % scatter plot or plot plot
    if sc == 0
        if marker == 0
            p = plot(x, y, 'o', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color); hold on;
            %e = errorbar(x,y,err,"o"); hold on;
        elseif marker == 1
            p = plot(x, y, 's', 'MarkerSize', sz, 'MarkerEdgeColor', color, 'MarkerFaceColor', color); hold on;
            %e = errorbar(x,y,err,"s"); hold on;
        end
    
    elseif sc == 1
        if marker == 0
            p = scatter(x, y, 10*sz,  cmap,'filled', 'Marker', 'o'); hold on;
        elseif marker == 1
            p = scatter(x, y, 10*sz,  cmap,'filled', 'Marker', 's'); hold on;
    end
    

end