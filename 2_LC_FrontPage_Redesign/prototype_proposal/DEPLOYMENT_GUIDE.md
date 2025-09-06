# Deployment Guide for LC Prototype

## 🚀 **Deployment Instructions**

### Target Location: `smartlessons.hkbu.tech/lc/demo.index`

### Files to Deploy:
- `demo_index.html` → Rename to `index.html` for deployment
- Assets folder (if any additional resources needed)

---

## 📋 **Pre-Deployment Checklist**

### Content Updates Needed:
1. **LC Corporate Video**
   - Replace video placeholder with actual LC corporate video
   - Recommended format: MP4 with WebM fallback
   - Optimal size: 1080p, under 50MB for web performance

2. **LC Head Photo & Message**
   - Professional headshot of Cissy Li (LC Head)
   - Personalized welcome message (300-400 words)
   - Contact information and office hours

3. **Toggle Content Customization**
   - Update News & Announcements with current information
   - Add real recent achievements and awards
   - Populate upcoming events calendar
   - Feature actual student success stories

---

## 🛠️ **GitHub Integration Steps**

### 1. Repository Setup
```bash
# Clone the smartLessons repository
git clone https://github.com/tesolchina/smartLessons.git

# Create LC demo branch
cd smartLessons
git checkout -b lc-prototype-demo

# Create LC directory structure  
mkdir -p lc/demo
```

### 2. File Deployment
```bash
# Copy prototype files
cp /path/to/demo_index.html lc/demo/index.html
cp /path/to/assets/* lc/demo/assets/ (if applicable)

# Add to git
git add lc/
git commit -m "Add LC front page redesign prototype"
git push origin lc-prototype-demo
```

### 3. Pull Request
- Create pull request to main branch
- Include prototype proposal document
- Request review from stakeholders

---

## 🌐 **Hosting Configuration**

### For smartlessons.hkbu.tech:
1. **DNS Setup**: Ensure subdomain points to correct server
2. **SSL Certificate**: Verify HTTPS configuration
3. **Server Configuration**: Enable proper MIME types for video
4. **Caching**: Set appropriate cache headers for performance

---

## 📊 **Testing Checklist**

### Desktop Testing:
- [ ] Chrome (latest)
- [ ] Safari (latest) 
- [ ] Firefox (latest)
- [ ] Edge (latest)

### Mobile Testing:
- [ ] iOS Safari
- [ ] Android Chrome
- [ ] Responsive design (320px - 1920px)

### Functionality Testing:
- [ ] Toggle sections expand/collapse
- [ ] Video placeholder displays correctly
- [ ] Navigation smooth scrolling
- [ ] Button interactions
- [ ] Mobile menu (if implemented)

### Performance Testing:
- [ ] Page load time < 3 seconds
- [ ] Lighthouse performance score > 90
- [ ] Images optimized and compressed
- [ ] CSS/JS minification (production)

---

## 🔧 **Production Optimization**

### Before Going Live:
1. **Minify CSS/JavaScript** for faster loading
2. **Optimize images** (WebP format recommended)
3. **Add meta tags** for SEO
4. **Test accessibility** (WAVE, axe tools)
5. **Validate HTML/CSS** for standards compliance

### Performance Enhancements:
- **Lazy loading** for images
- **Progressive video loading**
- **Service Worker** for caching (optional)
- **CDN integration** for static assets

---

## 📞 **Support & Maintenance**

### Technical Contact:
- **Primary Developer**: LC Website Team
- **Repository**: tesolchina/smartLessons
- **Branch**: lc-prototype-demo

### Content Updates:
- Toggle sections can be updated by editing HTML
- Video replacement requires file upload and HTML update
- Leadership message updates need HTML modification

### Future Iterations:
- WordPress integration planning
- CMS functionality for easy content updates
- User feedback integration
- A/B testing implementation

---

## 🎯 **Success Metrics to Monitor**

### After Deployment:
1. **User Engagement**
   - Time spent on page
   - Bounce rate
   - Toggle section interactions

2. **Performance Metrics**
   - Page load speed
   - Mobile responsiveness
   - Video completion rates

3. **Stakeholder Feedback**
   - LC staff reviews
   - Student user testing
   - Accessibility compliance

---

*Ready for deployment to smartlessons.hkbu.tech/lc/demo.index*  
*Version: 1.0 | Date: September 6, 2025*
