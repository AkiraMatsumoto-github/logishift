<?php
/**
 * The template for displaying the front page
 * SEO-optimized design based on content_strategy.md
 *
 * @package LogiShift
 */

get_header();
?>

<main id="primary" class="site-main">

	<!-- Hero Section -->
	<section class="hero-section">
		<div class="container">
			<div class="hero-content">
				<h1 class="hero-title"><?php esc_html_e( '物流DXで未来を創る LogiShift', 'logishift' ); ?></h1>
				<p class="hero-description"><?php esc_html_e( '倉庫管理・コスト削減・2024年問題対策まで。物流担当者と経営層のための実践的な課題解決メディア。', 'logishift' ); ?></p>
				<a href="#latest-articles" class="button hero-cta"><?php esc_html_e( '最新記事を読む', 'logishift' ); ?></a>
			</div>
		</div>
	</section>

	<!-- Featured Articles -->
	<section id="latest-articles" class="featured-articles-section">
		<div class="container">
			<div class="section-header">
				<h2 class="section-title"><?php esc_html_e( '注目記事', 'logishift' ); ?></h2>
			</div>

			<div class="featured-grid">
				<?php
				$featured_args = array(
					'post_type'      => 'post',
					'posts_per_page' => 3,
					'orderby'        => 'date',
					'order'          => 'DESC',
				);
				$featured_query = new WP_Query( $featured_args );

				if ( $featured_query->have_posts() ) :
					while ( $featured_query->have_posts() ) :
						$featured_query->the_post();
						?>
						<article id="post-<?php the_ID(); ?>" <?php post_class( 'featured-card' ); ?>>
							<div class="featured-thumbnail">
								<?php if ( has_post_thumbnail() ) : ?>
									<a href="<?php the_permalink(); ?>"><?php the_post_thumbnail( 'large' ); ?></a>
								<?php else : ?>
									<a href="<?php the_permalink(); ?>"><div class="no-image"></div></a>
								<?php endif; ?>
							</div>
							<div class="featured-content">
								<div class="article-meta">
									<?php
									$categories = get_the_category();
									if ( ! empty( $categories ) ) :
										?>
										<span class="cat-label"><?php echo esc_html( $categories[0]->name ); ?></span>
									<?php endif; ?>
									<span class="posted-on"><?php echo get_the_date(); ?></span>
								</div>
								<h3 class="featured-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
							</div>
						</article>
						<?php
					endwhile;
					wp_reset_postdata();
				endif;
				?>
			</div>
		</div>
	</section>

	<?php
	// Category sections based on content_strategy.md
	$category_sections = array(
		array(
			'slug'        => 'logistics-dx',
			'name'        => '物流DX・トレンド',
			'description' => '物流業界の最新動向、2024年問題、DX推進の実践的ノウハウ',
		),
		array(
			'slug'        => 'warehouse-management',
			'name'        => '倉庫管理・WMS',
			'description' => 'WMS導入、在庫管理、ピッキング効率化の成功事例',
		),
		array(
			'slug'        => 'transportation',
			'name'        => '輸配送・TMS',
			'description' => '配車計画、ラストワンマイル、動態管理の最適化手法',
		),
		array(
			'slug'        => 'material-handling',
			'name'        => 'マテハン・ロボット',
			'description' => '自動倉庫、AGV/AMR、RFID導入の最新トレンド',
		),
		array(
			'slug'        => 'supply-chain',
			'name'        => 'サプライチェーン',
			'description' => 'SCM戦略、調達最適化、国際物流のベストプラクティス',
		),
		array(
			'slug'        => 'case-studies',
			'name'        => '事例',
			'description' => '企業の成功事例、現場インタビュー、導入効果の実績',
		),
	);

	foreach ( $category_sections as $cat_section ) :
		$cat_obj = get_category_by_slug( $cat_section['slug'] );
		if ( ! $cat_obj ) {
			continue;
		}
		?>
		<section class="category-section category-<?php echo esc_attr( $cat_section['slug'] ); ?>">
			<div class="container">
				<div class="section-header">
					<div class="section-header-content">
						<h2 class="section-title"><?php echo esc_html( $cat_section['name'] ); ?></h2>
						<p class="section-description"><?php echo esc_html( $cat_section['description'] ); ?></p>
					</div>
					<a href="<?php echo esc_url( get_category_link( $cat_obj ) ); ?>" class="section-link"><?php esc_html_e( '一覧へ', 'logishift' ); ?> →</a>
				</div>

				<div class="article-grid">
					<?php
					$cat_args = array(
						'category_name'  => $cat_section['slug'],
						'posts_per_page' => 3,
						'orderby'        => 'date',
						'order'          => 'DESC',
					);
					$cat_query = new WP_Query( $cat_args );

					if ( $cat_query->have_posts() ) :
						while ( $cat_query->have_posts() ) :
							$cat_query->the_post();
							?>
							<article id="post-<?php the_ID(); ?>" <?php post_class( 'article-card' ); ?>>
								<div class="article-thumbnail">
									<?php if ( has_post_thumbnail() ) : ?>
										<a href="<?php the_permalink(); ?>"><?php the_post_thumbnail( 'medium' ); ?></a>
									<?php else : ?>
										<a href="<?php the_permalink(); ?>"><div class="no-image"></div></a>
									<?php endif; ?>
								</div>
								<div class="article-content">
									<div class="article-meta">
										<span class="posted-on"><?php echo get_the_date(); ?></span>
									</div>
									<h3 class="article-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
								</div>
							</article>
							<?php
						endwhile;
						wp_reset_postdata();
					else :
						?>
						<p class="no-posts"><?php esc_html_e( '記事がまだありません。', 'logishift' ); ?></p>
					<?php endif; ?>
				</div>
			</div>
		</section>
		<?php
	endforeach;
	?>

	<!-- Global Trends Section with Regional Filtering -->
	<section class="global-trends-section">
		<div class="container">
			<div class="section-header">
				<div class="section-header-content">
					<h2 class="section-title">🌍 <?php esc_html_e( '海外トレンド', 'logishift' ); ?></h2>
					<p class="section-description"><?php esc_html_e( '米国・欧州・アジアの最新物流DX事例と日本への示唆', 'logishift' ); ?></p>
				</div>
			</div>

			<!-- Regional Filter Tabs -->
			<div class="region-filter-tabs">
				<?php
				$global_cat = get_category_by_slug( 'news-global' );
				$global_url = $global_cat ? get_category_link( $global_cat ) : '#';
				?>
				<button class="region-tab active" data-region="all" data-url="<?php echo esc_url( $global_url ); ?>"><?php esc_html_e( 'すべて', 'logishift' ); ?></button>
				
				<?php
				$regions = array(
					'usa'            => array( 'label' => 'アメリカ', 'flag' => '🇺🇸' ),
					'europe'         => array( 'label' => 'ヨーロッパ', 'flag' => '🇪🇺' ),
					'china'          => array( 'label' => '中国', 'flag' => '🇨🇳' ),
					'southeast-asia' => array( 'label' => '東南アジア', 'flag' => '🌏' ),
				);

				foreach ( $regions as $slug => $info ) :
					$tag = get_term_by( 'slug', $slug, 'post_tag' );
					$url = $tag ? get_tag_link( $tag ) : '#';
					?>
					<button class="region-tab" data-region="<?php echo esc_attr( $slug ); ?>" data-url="<?php echo esc_url( $url ); ?>">
						<?php echo esc_html( $info['flag'] . ' ' . $info['label'] ); ?>
					</button>
				<?php endforeach; ?>
			</div>

			<div class="global-articles-container">
				<?php
				// Get all global trend articles with regional tags
				$global_args = array(
					'category_name'  => 'news-global',
					'posts_per_page' => 6,
					'orderby'        => 'date',
					'order'          => 'DESC',
				);
				$global_query = new WP_Query( $global_args );

				if ( $global_query->have_posts() ) :
					?>
					<div class="article-grid global-grid">
						<?php
						while ( $global_query->have_posts() ) :
							$global_query->the_post();
							$post_tags = get_the_tags();
							$region_tags = array();
							
							if ( $post_tags ) {
								foreach ( $post_tags as $tag ) {
									if ( in_array( $tag->slug, array( 'usa', 'europe', 'china', 'southeast-asia', 'japan', 'global' ) ) ) {
										$region_tags[] = $tag->slug;
									}
								}
							}
							
							$region_data = ! empty( $region_tags ) ? implode( ' ', $region_tags ) : 'all';
							?>
							<article id="post-<?php the_ID(); ?>" <?php post_class( 'article-card global-article' ); ?> data-regions="<?php echo esc_attr( $region_data ); ?>">
								<div class="article-thumbnail">
									<?php if ( has_post_thumbnail() ) : ?>
										<a href="<?php the_permalink(); ?>"><?php the_post_thumbnail( 'medium' ); ?></a>
									<?php else : ?>
										<a href="<?php the_permalink(); ?>"><div class="no-image"></div></a>
									<?php endif; ?>
								</div>
								<div class="article-content">
									<div class="article-meta">
										<?php if ( ! empty( $region_tags ) ) : ?>
											<span class="region-label"><?php echo esc_html( $region_tags[0] ); ?></span>
										<?php endif; ?>
										<span class="posted-on"><?php echo get_the_date(); ?></span>
									</div>
									<h3 class="article-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
								</div>
							</article>
							<?php
						endwhile;
						wp_reset_postdata();
						?>
					</div>
					
					<!-- Show More Button -->
					<div class="global-show-more-container" style="text-align: center; margin-top: 32px;">
						<a href="<?php echo esc_url( $global_url ); ?>" class="button outline global-show-more-link">
							<?php esc_html_e( 'もっと見る', 'logishift' ); ?> →
						</a>
					</div>

				<?php else : ?>
					<p class="no-posts"><?php esc_html_e( '記事がまだありません。', 'logishift' ); ?></p>
				<?php endif; ?>
			</div>
		</div>
	</section>

	<!-- Theme-based Tag Sections -->
	<section class="theme-tags-section">
		<div class="container">
			<div class="section-header">
				<h2 class="section-title"><?php esc_html_e( '課題別で探す', 'logishift' ); ?></h2>
			</div>

			<?php
			$theme_tags = array(
				array(
					'slug' => 'cost-reduction',
					'name' => 'コスト削減',
					'icon' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="theme-icon-svg"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>',
				),
				array(
					'slug' => 'labor-shortage',
					'name' => '人手不足対策',
					'icon' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="theme-icon-svg"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>',
				),
				array(
					'slug' => 'quality-improvement',
					'name' => '品質向上・誤出荷防止',
					'icon' => '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="theme-icon-svg"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="m9 12 2 2 4-4"></path></svg>',
				),
			);

			foreach ( $theme_tags as $theme_tag ) :
				?>
				<div class="theme-tag-block">
					<h3 class="theme-tag-title">
						<span class="theme-icon"><?php echo $theme_tag['icon']; ?></span>
						<?php echo esc_html( $theme_tag['name'] ); ?>
					</h3>
					<div class="theme-articles-scroll">
						<?php
						$tag_args = array(
							'tag'            => $theme_tag['slug'],
							'posts_per_page' => 4,
							'orderby'        => 'date',
							'order'          => 'DESC',
						);
						$tag_query = new WP_Query( $tag_args );

						if ( $tag_query->have_posts() ) :
							while ( $tag_query->have_posts() ) :
								$tag_query->the_post();
								?>
								<article class="theme-article-card">
									<div class="theme-article-thumbnail">
										<?php if ( has_post_thumbnail() ) : ?>
											<a href="<?php the_permalink(); ?>"><?php the_post_thumbnail( 'thumbnail' ); ?></a>
										<?php endif; ?>
									</div>
									<div class="theme-article-content">
										<h4 class="theme-article-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h4>
										<span class="theme-article-date"><?php echo get_the_date(); ?></span>
									</div>
								</article>
								<?php
							endwhile;
							wp_reset_postdata();
						endif;
						?>
					</div>
					<a href="<?php echo esc_url( get_tag_link( get_term_by( 'slug', $theme_tag['slug'], 'post_tag' ) ) ); ?>" class="theme-tag-link"><?php esc_html_e( 'もっと見る', 'logishift' ); ?> →</a>
				</div>
				<?php
			endforeach;
			?>
		</div>
	</section>

</main>

<script>
// Regional filter functionality with Mobile Limit
document.addEventListener('DOMContentLoaded', function() {
	const regionTabs = document.querySelectorAll('.region-tab');
	const globalArticles = document.querySelectorAll('.global-article');
	const showMoreLink = document.querySelector('.global-show-more-link');
	
	function filterArticles(selectedRegion) {
		let visibleCount = 0;
		const isMobile = window.matchMedia("(max-width: 768px)").matches;
		const limit = isMobile ? 3 : 999; // Limit to 3 on mobile

		globalArticles.forEach(article => {
			const articleRegions = article.getAttribute('data-regions');
			const shouldShow = (selectedRegion === 'all' || articleRegions.includes(selectedRegion));

			if (shouldShow) {
				// If strictly filtering (< limit), show. Else hide.
				if (visibleCount < limit) {
					article.style.display = 'block';
					visibleCount++;
				} else {
					article.style.display = 'none';
				}
			} else {
				article.style.display = 'none';
			}
		});

		// Update "Show More" Link
		if (showMoreLink) {
			const activeTab = document.querySelector('.region-tab[data-region="' + selectedRegion + '"]');
			if (activeTab && activeTab.dataset.url) {
				showMoreLink.href = activeTab.dataset.url;
				// Only show button if isMobile (since on PC we show all 6 anyway, but user experience wise "Show More" is good to keep or hide? 
				// User request: "スマホの場合... もっと見るを押した場合に... 遷移させる"
				// Let's keep it visible on PC too as it acts as "View Archive" which is useful.
				showMoreLink.style.display = 'inline-block';
			}
		}
	}

	regionTabs.forEach(tab => {
		tab.addEventListener('click', function() {
			const selectedRegion = this.getAttribute('data-region');
			
			// Update active tab
			regionTabs.forEach(t => t.classList.remove('active'));
			this.classList.add('active');
			
			filterArticles(selectedRegion);
		});
	});

	// Initial Filter
	filterArticles('all');

	// Re-filter on resize to adjust the limit
	let resizeTimeout;
	window.addEventListener('resize', function() {
		clearTimeout(resizeTimeout);
		resizeTimeout = setTimeout(function() {
			const activeTab = document.querySelector('.region-tab.active');
			const selectedRegion = activeTab ? activeTab.getAttribute('data-region') : 'all';
			filterArticles(selectedRegion);
		}, 200);
	});
});
</script>

<?php
get_footer();
