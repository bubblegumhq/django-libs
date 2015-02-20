__author__ = 'jawache'


class Resizer(object):

       def save_to_mem(self, img):
        """
        Saves PIL image to a ContentFile which can be saved to a django model
        """
        temp_handle = cStringIO.StringIO()
        img.save(temp_handle, 'JPEG', quality=100)
        return temp_handle

    # def save_to_storage(self, rootPath, content, dbObj):
    #     uuid = str(gen_unique_id())
    #     path = os.path.join(rootPath, uuid + ".jpg")
    #     cleanedPath = default_storage.save(path, content)
    #     dbObj.our_thumb_url = cleanedPath


    def rescale(self, img, width):
        """ Rescale the given image, optionally cropping it to make sure the result image has the specified width
        and height.
        """
        LOGGER.debug("Rescaling the image to %d width", width)
        img = img.convert("RGB")
        LOGGER.debug("Converted to RGB")
        src_width, src_height = img.size
        LOGGER.debug("%f, %f", src_width, src_height)


        # If width is less than the max then just sharpen and return
        if src_width <= width:
            LOGGER.debug("%f < %f", src_width, width)
            temp_handle = self.save_to_mem(img)
            return ContentFile(temp_handle.getvalue())

        # Else scale down then sharped and return
        scale_down = float(width) / float(src_width)
        dst_height = int(src_height * scale_down)
        LOGGER.debug("%f, %f", scale_down, dst_height)

        img = img.resize((width, dst_height), Image.ANTIALIAS)

        temp_handle = self.save_to_mem(img)
        return ContentFile(temp_handle.getvalue())


    def form_valid(self, form):
        url = form.cleaned_data['url']
        is_image = check_url_is_image_or_not(url)

        params = dict(
            source=url
        )
        if self.request.user.is_authenticated():
            params['user'] = self.request.user
        obj = Efographic.objects.create(**params)

        if is_image:
            response_image = None
            try:
                response_image = requests.get(url)
            except Exception, e:
                LOGGER.error("Error loading image %s" % url,exc_info=1)

            if not response_image or response_image.status_code != 200:

                if response_image.status_code == 403:
                    return render_to_response(self.template_name,
                                              {'error': "This URL returns a permission denied error, the admin of that URL doesn't allow other sites to take pictures of their page or grab a copy of their image.",
                                               'form':form,
                                               'url': url},
                                              context_instance=RequestContext(self.request))
                else:
                    return render_to_response(self.template_name,
                                              {'error': "This url returned an error, please make sure it exists and you don't have a problem viewing it",
                                               'form':form,
                                               'url': url},
                                              context_instance=RequestContext(self.request))

            image_content = response_image.content
            file = self.rescale(Image.open(cStringIO.StringIO(image_content)), 1000)
            ext = url.split('.')[-1]
            obj.original_image.save(shortuuid.uuid() + '.' + ext, file)
        else:
            # Take snapshot
            image_name = take_snapshot(url)

            image_path = os.path.join('/tmp', image_name)

            with open(image_path) as f:
                file = self.rescale(Image.open(cStringIO.StringIO(f.read())), 1000)
                obj.original_image.save(image_name, file)

            # Delete the image from tmp directory
            try:
                os.remove(image_path)
            except OSError:
                pass

        return redirect(obj.get_step2_url())

