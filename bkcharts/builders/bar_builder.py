from bkcharts.builders import bar_builder
from bkcharts.utils import add_tooltips_columns
class ToolTipBar(bar_builder.BarBuilder):
    def yield_renderers(self):
        """Use the rect glyphs to display the bars.
        Takes reference points from data loaded at the ColumnDataSource.
        """
        kwargs = self.get_extra_args()
        attrs = self.collect_attr_kwargs()

        for group in self._data.groupby(**self.attributes):
            glyph_kwargs = self.get_group_kwargs(group, attrs)
            group_kwargs = kwargs.copy()
            group_kwargs.update(glyph_kwargs)
            props = self.glyph.properties().difference(set(['label']))

            # make sure we always pass the color and line color
            for k in ['color', 'line_color']:
                group_kwargs[k] = group[k]

            # TODO(fpliger): we shouldn't need to do this to ensure we don't
            #               have extra kwargs... this is needed now because
            #               of label, group and stack being "special"
            for k in set(group_kwargs):
                if k not in props:
                    group_kwargs.pop(k)

            bg = self.glyph(label=group.label,
                            x_label=self._get_label(group['label']),
                            values=group.data[self.values.selection].values,
                            agg=stats[self.agg](),
                            width=self.bar_width,
                            fill_alpha=self.fill_alpha,
                            stack_label=self._get_label(group['stack']),
                            dodge_label=self._get_label(group['group']),
                            **group_kwargs)

            self.add_glyph(group, bg)

        if self._perform_stack:
            Stack().apply(self.comp_glyphs)
        if self._perform_group:
            Dodge().apply(self.comp_glyphs)

        # a higher level function of bar chart is to keep track of max height of all bars
        self.max_height = max([renderer.y_max for renderer in self.comp_glyphs])
        self.min_height = min([renderer.y_min for renderer in self.comp_glyphs])
        

        for renderer in self.comp_glyphs:
            if self.tooltips:
                    renderer = add_tooltips_columns(renderer, self.tooltips, group)
            for sub_renderer in renderer.renderers:
                yield sub_renderer
def generate_bar_from_scratch():
    p = figure(plot_width=400, plot_height=400)
    p.square([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="olive", alpha=0.5)
    return p
