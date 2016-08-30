/*
 * Copyright (C) 2016  Fridolin Pokorny, fpokorny@redhat.com
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */

// TODO: propagate error in configuration to a modal window
// TODO: warning before uploading about worker restart

$('#flow-preview').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var flow_name = button.data('flowname');
  var modal = $(this);

  modal.find('.modal-title').text("Flow preview for flow " + flow_name)
  modal.find('.modal-body img').attr("src", "/graph/" + flow_name + ".png")
});

$('#flow-run').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var flow_name = button.data('flowname');
  var modal = $(this);

  modal.find('.modal-title').text("Run flow " + flow_name)
  modal.find('#flow-run-name').attr("value", flow_name)
});

$('#system-conf').on('show.bs.modal', function (event) {
  var modal = $(this);

  // no need to query for the same again
  if (modal.find('#system-conf-flow li').length > 0)
    return;

  var listing = modal.find('#system-conf-flow');

  $.ajax({
    url: "/config-files",
    cache: false,
    dataType: "json",
    success: function(data) {

      modal.find('#system-conf-nodes').append($('<li>')
                                          .append($('<a>')
                                              .attr('href', "/config-file/" + data['nodes'])
                                              .text(data['nodes'])
                                              )
                                          );

      data['flows'].sort();
      for (i = 0; i < data['flows'].length; i++) {
        listing.append($('<li>')
                   .append($('<a>')
                       .attr('href', "/config-file/" + data['flows'][i])
                       .text(data['flows'][i])
                       )
                   );
      }
    }
  });
});

$('#flow-run-button').click(function(e) {
  $.ajax({
    type: "POST",
    url: "/run/" + $('#flow-run-name').attr('value'),
    data: $("#flow-run-form").serialize(),
    dataType: "json",
    success: function(response) {
      if ('error' in response)
        $('#flow-info-text p').text('There was an error with flow run: ' + response['error']);
      else
        $('#flow-info-text p').html('Flow has successfully started. ' +
                                    'Dispatcher id is <code>' + response['dispatcher_id'] + '</code>.');

      $('#flow-run').modal('hide');
      $('#flow-info').modal('show');
    },
    error: function(what) {
      console.log(what);
      $('#flow-info-text p').text('There was an error when starting flow. Refer to logs for more info.');

      $('#flow-run').modal('hide');
      $('#flow-info-text').modal('show');
    }
  });
});
