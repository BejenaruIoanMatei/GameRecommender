#!/usr/bin/perl
use strict;
use warnings;
use LWP::UserAgent;
use JSON;

sub test_endpoint {
    my ($method, $url, $data, $outfile) = @_;
    
    my $ua = LWP::UserAgent->new(timeout => 10);
    my $response;
    
    if ($method eq 'GET') {
        $response = $ua->get($url);
    } elsif ($method eq 'POST') {
        $response = $ua->post($url, 
            'Content-Type' => 'application/json',
            Content => encode_json($data)
        );
    }
    
    print "Status: " . $response->code . "\n";

    my $content = $response->decoded_content;

    print "Response:\n$content\n";

    eval {
        my $json_data = decode_json($content);
        my $pretty_json = to_json($json_data, { pretty => 1, utf8 => 1 });

        open(my $fh, '>:encoding(UTF-8)', $outfile) or die "Nu pot deschide fișierul '$outfile' pentru scriere: $!";
        print $fh $pretty_json;
        close($fh);

        print "Saved response to $outfile\n";
    };
    if ($@) {
        warn "Nu am putut decoda JSON: $@\n";
        open(my $fh, '>:encoding(UTF-8)', $outfile) or die "Nu pot deschide fișierul '$outfile' pentru scriere: $!";
        print $fh $content;
        close($fh);

        print "Saved raw response to $outfile\n";
    }

    return $response->is_success;
}

test_endpoint('GET', 'http://127.0.0.1:8000/recommend/cosine?title=the%20crew%202', undef, 'test/response_cosine.json');
test_endpoint('GET', 'http://127.0.0.1:8000/recommend/nn?title=the%20crew%202', undef, 'test/response_nn.json');
